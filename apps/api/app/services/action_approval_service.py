from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.action_models import ActionApproval, ActionLog
from app.models.action_execution_state import ActionExecutionStatus
from app.services.action_observability_service import ActionObservabilityService
from datetime import datetime, timezone

class ActionApprovalService:
    @classmethod
    async def create_approval_request(cls, db: AsyncSession, action_log_id: str, user_id: str) -> ActionApproval:
        approval = ActionApproval(
            action_log_id=action_log_id,
            user_id=user_id,
            status="pending"
        )
        db.add(approval)
        await db.commit()
        await db.refresh(approval)
        return approval

    @classmethod
    async def decide_approval(cls, db: AsyncSession, approval_id: str, approve: bool) -> bool:
        result = await db.execute(select(ActionApproval).where(ActionApproval.id == approval_id))
        approval = result.scalar_one_or_none()
        if not approval or approval.status != "pending":
            return False
            
        now = datetime.now(timezone.utc)
        approval.status = "approved" if approve else "rejected"
        approval.decided_at = now
        
        # Calculate approval latency
        latency_ms = 0.0
        if approval.created_at:
            # Force timezone awareness to match 'now'
            created_aware = approval.created_at.replace(tzinfo=timezone.utc) if approval.created_at.tzinfo is None else approval.created_at
            latency_ms = (now - created_aware).total_seconds() * 1000.0
        
        # Selectively update linked ActionLog approval status parameter
        log_res = await db.execute(select(ActionLog).where(ActionLog.id == approval.action_log_id))
        log = log_res.scalar_one_or_none()
        if log:
            log.approval_status = "approved" if approve else "rejected"
            if approve:
                log.approved_at = now
                log.execution_status = ActionExecutionStatus.QUEUED
                log.queued_at = now
                await db.commit()
                
                ActionObservabilityService.log_event(
                    event_name="action_approved",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id,
                    extra={"latency_ms": latency_ms}
                )
                ActionObservabilityService.log_event(
                    event_name="action_queued",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id
                )
                
                from app.services.job_enqueuer import JobEnqueuer
                await JobEnqueuer.enqueue_action(
                    action_log_id=log.id,
                    action_name=log.action_name,
                    user_id=log.user_id,
                    idempotency_key=log.idempotency_key
                )
                return True
            else:
                log.status = "failed"
                log.execution_status = ActionExecutionStatus.FAILED
                log.failed_at = now
                log.completed_at = now
                log.error_message = "Rejected by user approval decision."
                await db.commit()
                
                ActionObservabilityService.log_event(
                    event_name="action_rejected",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id,
                    extra={"latency_ms": latency_ms}
                )
                return True
            
        await db.commit()
        return True
