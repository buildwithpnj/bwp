import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus
from app.services.job_enqueuer import JobEnqueuer
from app.services.action_observability_service import ActionObservabilityService

logger = logging.getLogger("dead_letter_service")

class DeadLetterService:
    @classmethod
    async def move_to_dlq(cls, db: AsyncSession, log: ActionLog, reason: str) -> None:
        """Moves an action log to dead-letter state."""
        log.execution_status = ActionExecutionStatus.PERMANENTLY_FAILED
        log.dead_lettered_at = datetime.now(timezone.utc)
        log.last_error = f"DLQ: {reason}"
        await db.commit()
        
        logger.warning(f"Action log={log.id} dead-lettered. Reason: {reason}")
        ActionObservabilityService.log_event(
            event_name="action_dead_lettered",
            user_id=log.user_id,
            action_name=log.action_name,
            action_log_id=log.id,
            extra={"reason": reason}
        )

    @classmethod
    async def list_dlq_logs(cls, db: AsyncSession, limit: int = 50, offset: int = 0) -> List[ActionLog]:
        """Lists permanently failed or dead-lettered logs."""
        stmt = select(ActionLog).where(
            ActionLog.dead_lettered_at.isnot(None)
        ).order_by(ActionLog.dead_lettered_at.desc()).limit(limit).offset(offset)
        
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @classmethod
    async def replay_dlq_job(cls, db: AsyncSession, log_id: str) -> bool:
        """Resets retry count and re-enqueues a dead-lettered job for execution."""
        stmt = select(ActionLog).where(ActionLog.id == log_id)
        res = await db.execute(stmt)
        log = res.scalar_one_or_none()
        
        if not log or log.dead_lettered_at is None:
            logger.error(f"Cannot replay: log ID={log_id} is not in DLQ")
            return False
            
        logger.info(f"Replaying DLQ job for action_log={log.id}")
        
        # Reset counters and state
        log.retry_count = 0
        log.execution_status = ActionExecutionStatus.QUEUED
        log.dead_lettered_at = None
        await db.commit()
        
        ActionObservabilityService.log_event(
            event_name="action_dlq_replayed",
            user_id=log.user_id,
            action_name=log.action_name,
            action_log_id=log.id
        )
        
        # Queue the job again
        await JobEnqueuer.enqueue_action(
            action_log_id=log.id,
            action_name=log.action_name,
            user_id=log.user_id,
            idempotency_key=log.idempotency_key
        )
        return True
