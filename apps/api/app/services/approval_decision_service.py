import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.models.action_approval_models import ActionApprovalRequest
from app.models.action_models import ActionLog
from app.services.approval_gate_service import ApprovalGateService
from app.services.approval_request_service import ApprovalRequestService
from app.services.action_execution_service import ActionExecutionService
from app.services.ui_action_bridge import UiActionBridge
from app.services.action_audit_log_service import ActionAuditLogService
from app.services.approval_metrics_service import ApprovalMetricsService

logger = logging.getLogger("approval_decision_service")

class ApprovalDecisionService:
    @classmethod
    async def decide(
        cls,
        db: AsyncSession,
        approval_id: str,
        approve: bool,
        actor_id: str,
        token: str
    ) -> Dict[str, Any]:
        """
        Processes Allow/Deny decisions for action execution.
        """
        # Retrieve the request
        req = await ApprovalRequestService.get_request(db, approval_id)
        if not req:
            return {"status": "failed", "error": "Approval request not found."}

        # Validate token and user permission bounds
        token_approval_id = ApprovalGateService.validate_approval_token(token, req.user_id, req.tenant_id)
        if not token_approval_id or token_approval_id != approval_id:
            ApprovalMetricsService.increment_leak_prevention_count()
            return {"status": "failed", "error": "Invalid, expired, or replayed approval token."}

        if req.status != "pending":
            return {"status": "failed", "error": f"Approval request is already in '{req.status}' state."}

        # Check request expiry
        if datetime.now(timezone.utc) > req.expires_at:
            req.status = "expired"
            await db.commit()
            ApprovalMetricsService.increment_expired_count()
            return {"status": "failed", "error": "Approval request has expired."}

        # Handle Denied state
        if not approve:
            req.status = "denied"
            req.denied_by = actor_id
            
            # Update ActionLog
            if req.action_log_id:
                stmt = select(ActionLog).where(ActionLog.id == req.action_log_id)
                res = await db.execute(stmt)
                log = res.scalar_one_or_none()
                if log:
                    log.status = "failed"
                    log.error_message = "Action denied. No changes were made."
            
            await db.commit()
            ApprovalMetricsService.increment_denied_count()
            return {"status": "denied", "message": "Action denied. No changes were made."}

        # Handle Approved state -> Execute & Verify
        req.status = "approved"
        req.approved_by = actor_id
        await db.flush()

        if not req.action_log_id:
            return {"status": "failed", "error": "No linked ActionLog found for this approval request."}

        stmt = select(ActionLog).where(ActionLog.id == req.action_log_id)
        res = await db.execute(stmt)
        log = res.scalar_one_or_none()
        if not log:
            return {"status": "failed", "error": "Linked ActionLog not found."}

        try:
            # Execute original action payload
            exec_res = await ActionExecutionService.execute_log_action(db, log)
            if isinstance(exec_res, dict) and exec_res.get("status") == "failed":
                req.status = "failed"
                log.status = "failed"
                log.error_message = exec_res.get("error", "Execution failed")
                await db.commit()
                return {"status": "failed", "error": log.error_message}

            # Factual verification of the side effect
            is_verified = await UiActionBridge.verify_action_outcome(db, req.action_name, req.action_payload, req.user_id)
            if not is_verified:
                req.status = "failed"
                log.status = "failed"
                log.error_message = "This action could not be verified after execution."
                await db.commit()
                ApprovalMetricsService.increment_verifier_failure_count()
                return {"status": "failed", "error": "This action could not be verified after execution."}

            # Success transitions
            req.status = "executed"
            log.status = "success"
            await db.commit()

            # Increment metrics
            ApprovalMetricsService.increment_approved_count()
            
            # Log audit
            ActionAuditLogService.log_execution(req.action_name, req.action_payload, req.tenant_id or "default_tenant")
            
            return {"status": "success", "message": "Action approved and executed successfully."}

        except Exception as e:
            req.status = "failed"
            log.status = "failed"
            log.error_message = str(e)
            await db.commit()
            return {"status": "failed", "error": str(e)}
