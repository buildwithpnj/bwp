from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.action_approval_models import ActionApprovalRequest
from app.models.action_models import ActionLog
from app.services.approval_metrics_service import ApprovalMetricsService

class ApprovalExpiryService:
    @classmethod
    async def expire_pending_requests(cls, db: AsyncSession) -> int:
        """
        Scans the database for pending approval requests that have exceeded their lifespans,
        transitions their status to 'expired', updates linked ActionLogs, and logs telemetry.
        """
        now = datetime.now(timezone.utc)
        stmt = select(ActionApprovalRequest).where(
            ActionApprovalRequest.status == "pending",
            ActionApprovalRequest.expires_at < now
        )
        res = await db.execute(stmt)
        expired_reqs = res.scalars().all()
        
        count = 0
        for req in expired_reqs:
            req.status = "expired"
            count += 1
            ApprovalMetricsService.increment_expired_count()
            
            # Update linked ActionLog to failed/expired
            if req.action_log_id:
                stmt_log = select(ActionLog).where(ActionLog.id == req.action_log_id)
                res_log = await db.execute(stmt_log)
                log = res_log.scalar_one_or_none()
                if log:
                    log.status = "failed"
                    log.error_message = "Approval request expired. No changes were made."

        if count > 0:
            await db.commit()
            
        return count
