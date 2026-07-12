from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.deps import CurrentUser, DB
from app.services.agent_english_service import AgentEnglishService
from app.services.warborn_session_service import WarbornSessionService
from app.services.agent_memory_context_builder import AgentMemoryContextBuilder
from app.services.action_execution_service import ActionExecutionService
from app.services.action_approval_service import ActionApprovalService
from typing import Optional, Dict, Any

router = APIRouter(prefix="/api/warborn", tags=["Warborn Chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    message: str
    status: str
    suggested_action: Optional[Dict[str, Any]] = None

class ActionRequestSchema(BaseModel):
    action_name: str
    payload: Dict[str, Any]

class ActionApprovalSchema(BaseModel):
    approval_id: str
    approve: bool

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, current_user: CurrentUser, db: DB):
    # Enforce role entitlements gating
    if current_user.role not in ["approved_user", "internal_admin"]:
        raise HTTPException(status_code=403, detail="System access pending approval.")

    # Verify session ownership/permissions
    session = WarbornSessionService.get_session(req.session_id)
    if not session or session["user_id"] != current_user.id:
        sess_id = WarbornSessionService.create_session(current_user.id)
        req.session_id = sess_id
        
    context_block = await AgentMemoryContextBuilder.build_context_block(db, current_user.id)
    full_message = f"{context_block}\n\nUser Input: {req.message}" if context_block else req.message
        
    res = await AgentEnglishService.respond_to_authenticated(
        session_id=req.session_id,
        message=full_message
    )
    
    # Analyze user input and return a suggested action if matching intent
    suggestion = None
    cleaned_input = req.message.lower()
    if "correct grammar:" in cleaned_input:
        suggestion = {
            "action_name": "save_corrected_example",
            "payload": {
                "original": req.message.replace("correct grammar:", "").strip(),
                "corrected": res["message"].strip(),
                "explanation": "Grammar corrected and stored to user vocabulary log."
            }
        }
    elif "preference" in cleaned_input:
        suggestion = {
            "action_name": "update_preference",
            "payload": {
                "tone": "professional",
                "explanation_style": "brief"
            }
        }
    elif "practice" in cleaned_input:
        # reminder actions require manual approvals
        suggestion = {
            "action_name": "create_followup_practice",
            "payload": {
                "task_description": "Review article mistakes practiced during this session."
            }
        }
    
    return ChatResponse(
        message=res["message"],
        status=res["status"],
        suggested_action=suggestion
    )

@router.post("/action/execute")
async def execute_action(req: ActionRequestSchema, current_user: CurrentUser, db: DB):
    if current_user.role not in ["approved_user", "internal_admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized role context.")
        
    res = await ActionExecutionService.request_execution(
        db=db,
        user_id=current_user.id,
        user_role=current_user.role,
        action_name=req.action_name,
        payload=req.payload
    )
    return res

@router.post("/action/approve")
async def approve_action(req: ActionApprovalSchema, current_user: CurrentUser, db: DB):
    if current_user.role not in ["approved_user", "internal_admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized role context.")
        
    ok = await ActionApprovalService.decide_approval(db, req.approval_id, req.approve)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid approval request or already processed.")
    return {"status": "success"}
