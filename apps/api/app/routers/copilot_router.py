from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, Optional
from app.deps import CurrentUser, DB
from app.schemas.copilot_context_payload import CopilotContextPayload
from app.services.copilot_session_service import CopilotSessionService
from app.services.copilot_router_service import CopilotRouterService
from app.services.ui_action_bridge import UiActionBridge
from app.services.voice_session_service import VoiceSessionService
from app.services.action_response_formatter import ActionResponseFormatter
from app.services.approval_decision_service import ApprovalDecisionService
from app.schemas.action_approval_schemas import ApprovalDecisionInput

router = APIRouter(prefix="/api/copilot", tags=["Global Dashboard Copilot"])

async def process_and_bridge_action(
    db: DB,
    action: Optional[Dict[str, Any]],
    user_id: str,
    session_id: str,
    reply_text: str
):
    act_log_id = None
    approval_required = False
    approval_request = None
    token = None
    
    if action:
        res = await UiActionBridge.bridge_action_to_runner_v0501(
            db, action["action_name"], action["payload"], user_id, session_id
        )
        act_log_id = res.get("action_log_id")
        
        if res.get("status") == "pending_approval":
            approval_required = True
            approval_request = res.get("approval_request")
            token = res.get("token")
            reply_text = ActionResponseFormatter.format_response(
                status="confirm",
                action_name=action["action_name"],
                result="Action requires approval before execution.",
                next_steps="Review the requested change below."
            )
        elif res.get("status") == "blocked":
            approval_required = False
            action = None
            reply_text = ActionResponseFormatter.format_response(
                status="blocked",
                action_name=res.get("action_name", "action"),
                result="This request is blocked by policy."
            )
        elif res.get("status") == "success":
            reply_text = ActionResponseFormatter.format_response(
                status="success",
                action_name=action["action_name"],
                result="Action approved and executed successfully."
            )
        elif res.get("status") == "failed":
            reply_text = ActionResponseFormatter.format_response(
                status="failed",
                action_name=action["action_name"],
                result=res.get("message", "Action execution failed.")
            )
            
    return reply_text, action, act_log_id, approval_required, approval_request, token

@router.post("/chat", status_code=status.HTTP_200_OK)
async def submit_copilot_query(
    query: str,
    ctx: CopilotContextPayload,
    current_user: CurrentUser,
    db: DB
):
    """
    Submits route-aware copilot query. Auto-executes safe actions, blocks admin-only,
    and returns approval cards for confirmation-required actions.
    """
    sess = await CopilotSessionService.get_or_create_session(db, current_user.id)
    
    # Process route & query
    reply_text, action = await CopilotRouterService.process_query(
        db, query, ctx, current_user.id, sess.chat_history
    )
    
    # Run the risk classifier and execution bridge
    reply_text, action, act_log_id, approval_required, approval_request, token = await process_and_bridge_action(
        db, action, current_user.id, sess.id, reply_text
    )
    
    # Save history
    await CopilotSessionService.append_message(db, sess, "user", query)
    await CopilotSessionService.append_message(db, sess, "assistant", reply_text, action)
    
    return {
        "reply": reply_text,
        "suggested_action": action,
        "action_log_id": act_log_id,
        "session_id": sess.id,
        "approval_required": approval_required,
        "approval_request": approval_request,
        "token": token
    }

@router.post("/voice", status_code=status.HTTP_200_OK)
async def submit_voice_stream(
    ctx: CopilotContextPayload,
    current_user: CurrentUser,
    db: DB
):
    """
    Simulates speech-to-text trigger for voice interaction on current view contexts.
    """
    sess = await CopilotSessionService.get_or_create_session(db, current_user.id)
    
    transcription = VoiceSessionService.transcribe_audio_chunk(b"")
    reply_text, action = await CopilotRouterService.process_query(
        db, transcription, ctx, current_user.id, sess.chat_history
    )
    
    # Run risk classifier and execution bridge
    reply_text, action, act_log_id, approval_required, approval_request, token = await process_and_bridge_action(
        db, action, current_user.id, sess.id, reply_text
    )
    
    await CopilotSessionService.append_message(db, sess, "user", transcription)
    await CopilotSessionService.append_message(db, sess, "assistant", reply_text, action)
    
    return {
        "transcription": transcription,
        "reply": reply_text,
        "suggested_action": action,
        "action_log_id": act_log_id,
        "session_id": sess.id,
        "approval_required": approval_required,
        "approval_request": approval_request,
        "token": token
    }

@router.post("/approve", status_code=status.HTTP_200_OK)
async def decide_approval_request(
    approval_id: str,
    payload: ApprovalDecisionInput,
    current_user: CurrentUser,
    db: DB
):
    """
    Allows or denies a pending action execution request using single-use tokens.
    """
    res = await ApprovalDecisionService.decide(
        db=db,
        approval_id=approval_id,
        approve=payload.approve,
        actor_id=current_user.id,
        token=payload.token
    )
    
    if res.get("status") == "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("error", "Failed to resolve approval request.")
        )
        
    return res
