import logging
import time
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus
from app.services.job_enqueuer import JobEnqueuer
from app.services.failure_recovery_service import FailureRecoveryService

logger = logging.getLogger("recovery_worker")

class RecoveryWorker:
    @classmethod
    async def recover_stale_jobs(cls, db: AsyncSession, max_stale_minutes: int = 5) -> int:
        """
        Scans for action logs stuck in EXECUTING or QUEUED state and triggers recovery.
        Returns:
            int: Number of recovered jobs.
        """
        threshold = datetime.now(timezone.utc) - timedelta(minutes=max_stale_minutes)
        
        stmt = select(ActionLog).where(
            ActionLog.execution_status.in_([ActionExecutionStatus.EXECUTING, ActionExecutionStatus.QUEUED]),
            ActionLog.updated_at < threshold
        )
        
        res = await db.execute(stmt)
        stale_logs = res.scalars().all()
        
        count = 0
        for log in stale_logs:
            logger.warning(f"RecoveryWorker found stale log ID={log.id} state={log.execution_status}")
            
            # Reset and re-queue, or trigger rollback recovery
            if log.retry_count < log.max_retries:
                log.retry_count += 1
                log.execution_status = ActionExecutionStatus.QUEUED
                log.recovery_status = ActionRecoveryStatus.PENDING_RECOVERY
                await db.commit()
                
                # Re-queue the job
                await JobEnqueuer.enqueue_action(
                    action_log_id=log.id,
                    action_name=log.action_name,
                    user_id=log.user_id,
                    idempotency_key=log.idempotency_key
                )
                count += 1
            else:
                # Trigger rollback recovery immediately
                log.execution_status = ActionExecutionStatus.PERMANENTLY_FAILED
                await db.commit()
                await FailureRecoveryService.process_failure(
                    db, log, Exception("Stale execution timeout exceeded max retries.")
                )
                count += 1
                
        return count
