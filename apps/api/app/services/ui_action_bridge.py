import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional

from app.models.action_models import ActionLog
from app.models.notes import Note
from app.models.goals import Goal
from app.services.action_execution_service import ActionExecutionService
from app.services.action_risk_classifier import ActionRiskClassifier
from app.services.action_policy_registry import ActionPolicyTier
from app.services.approval_request_service import ApprovalRequestService
from app.services.approval_token_service import ApprovalTokenService
from app.services.action_result_verifier import ActionResultVerifier
from app.services.action_audit_log_service import ActionAuditLogService

logger = logging.getLogger("ui_action_bridge")

class UiActionBridge:
    @classmethod
    async def bridge_action_to_runner(
        cls,
        db: AsyncSession,
        action_name: str,
        payload: Dict[str, Any],
        user_id: str
    ) -> str:
        """
        Legacy entrypoint. Adapts to redirect to the new v0.50.1 approval logic.
        """
        res = await cls.bridge_action_to_runner_v0501(db, action_name, payload, user_id)
        return res.get("action_log_id", "")

    @classmethod
    async def bridge_action_to_runner_v0501(
        cls,
        db: AsyncSession,
        action_name: str,
        payload: Dict[str, Any],
        user_id: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes Copilot actions through the permanent risk/approval pipeline.
        - SAFE_AUTO: Executes immediately, runs verification, records audit.
        - CONFIRM_FIRST / DESTRUCTIVE_CONFIRMED: Pauses execution, creates ApprovalRequest + Token.
        - ADMIN_ONLY: Blocked unless user is 'admin_user' or has admin permissions.
        """
        policy = ActionRiskClassifier.classify_action(action_name, payload)
        tenant_id = f"tenant_{user_id.split('_')[-1]}" if "_" in user_id else "default_tenant"

        log_id = f"act_{uuid.uuid4().hex[:8]}"
        log = ActionLog(
            id=log_id,
            user_id=user_id,
            tenant_id=tenant_id,
            action_name=action_name,
            input_payload=payload,
            status="pending",
            approval_status="pending"
        )

        # ADMIN_ONLY policy check
        if policy == ActionPolicyTier.ADMIN_ONLY:
            # Enforce admin privilege check
            if user_id != "admin_user" and not user_id.endswith("_admin"):
                log.status = "failed"
                log.approval_status = "rejected"
                log.error_message = "This request is blocked by policy."
                db.add(log)
                await db.commit()
                # Log audit
                ActionAuditLogService.log_execution(action_name, payload, tenant_id)
                return {
                    "status": "blocked",
                    "message": "This request is blocked by policy.",
                    "action_log_id": log_id
                }

        # SAFE_AUTO policy check -> auto execute
        if policy == ActionPolicyTier.SAFE_AUTO:
            log.approval_status = "auto_approved"
            db.add(log)
            await db.flush()
            
            try:
                res = await ActionExecutionService.execute_log_action(db, log)
                if isinstance(res, dict) and res.get("status") == "failed":
                    log.status = "failed"
                    log.error_message = res.get("error", "Execution failed")
                    await db.commit()
                    return {"status": "failed", "message": log.error_message, "action_log_id": log_id}
                
                # Factual verification step
                is_verified = await cls.verify_action_outcome(db, action_name, payload, user_id)
                if not is_verified:
                    log.status = "failed"
                    log.error_message = "This action could not be verified after execution."
                    await db.commit()
                    return {
                        "status": "failed", 
                        "message": "This action could not be verified after execution.", 
                        "action_log_id": log_id
                    }
                
                log.status = "success"
                await db.commit()
                ActionAuditLogService.log_execution(action_name, payload, tenant_id)
                return {"status": "success", "action_log_id": log_id}
            except Exception as e:
                log.status = "failed"
                log.error_message = str(e)
                await db.commit()
                return {"status": "failed", "message": str(e), "action_log_id": log_id}

        # CONFIRM_FIRST & DESTRUCTIVE_CONFIRMED require Allow/Deny dialog
        log.approval_status = "pending"
        db.add(log)
        await db.flush()

        # Create request and single-use token
        req = await ApprovalRequestService.create_request(
            db=db,
            user_id=user_id,
            action_name=action_name,
            payload=payload,
            tenant_id=tenant_id,
            session_id=session_id,
            action_log_id=log_id
        )
        
        token = ApprovalTokenService.generate_token(req.id, user_id, tenant_id)
        await db.commit()

        ActionAuditLogService.log_execution(action_name, payload, tenant_id)
        
        return {
            "status": "pending_approval",
            "action_log_id": log_id,
            "token": token,
            "approval_request": {
                "id": req.id,
                "action_name": req.action_name,
                "policy_tier": req.policy_tier,
                "risk_level": req.risk_level,
                "human_summary": req.human_summary,
                "execution_preview": req.execution_preview,
                "expires_at": req.expires_at.isoformat()
            }
        }

    @classmethod
    async def verify_action_outcome(
        cls, 
        db: AsyncSession, 
        action_name: str, 
        payload: Dict[str, Any], 
        user_id: str
    ) -> bool:
        """
        Routes verification checks to ActionResultVerifier.
        """
        try:
            if action_name == "create_note":
                stmt = select(Note).where(Note.user_id == user_id, Note.title == payload.get("title"))
                res = await db.execute(stmt)
                return res.scalar_one_or_none() is not None
            elif action_name == "create_task":
                stmt = select(Goal).where(Goal.user_id == user_id, Goal.title == payload.get("title"))
                res = await db.execute(stmt)
                return res.scalar_one_or_none() is not None
            elif action_name == "update_task":
                task_id = payload.get("task_id")
                expected_status = payload.get("status")
                return await ActionResultVerifier.verify_task_status(db, task_id, expected_status)
            elif action_name == "delete_note":
                note_id = payload.get("note_id")
                return await ActionResultVerifier.verify_note_deleted(db, note_id, user_id)
            elif action_name == "delete_task":
                task_id = payload.get("task_id")
                return await ActionResultVerifier.verify_task_deleted(db, task_id, user_id)
            elif action_name == "restore_note":
                note_id = payload.get("note_id")
                return await ActionResultVerifier.verify_trash_item_restored(db, "note", note_id, user_id)
            elif action_name == "restore_task":
                task_id = payload.get("task_id")
                return await ActionResultVerifier.verify_trash_item_restored(db, "task", task_id, user_id)
            elif action_name == "search_knowledge":
                return True
        except Exception as e:
            logger.error(f"Action verifier hit exception: {e}")
            return False
            
        return True
