import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.action_models import ActionLog
from app.services.delay_policy import DelayPolicy
from app.services.job_enqueuer import JobEnqueuer

logger = logging.getLogger("worker_retry_scheduler")

class WorkerRetryScheduler:
    @classmethod
    async def schedule_retry(cls, db: AsyncSession, log: ActionLog) -> str:
        """
        Schedules a retry for a failed action log using exponential backoff.
        """
        delay = DelayPolicy.calculate_delay(log.retry_count)
        now = datetime.now(timezone.utc)
        scheduled_time = now + timedelta(seconds=delay)
        
        # Update log timestamps
        log.retry_scheduled_at = scheduled_time
        await db.commit()
        
        logger.info(f"Scheduling retry for action_log={log.id} in {delay} seconds (at {scheduled_time})")
        
        # Enqueue with delay
        job_id = await JobEnqueuer.enqueue_action(
            action_log_id=log.id,
            action_name=log.action_name,
            user_id=log.user_id,
            idempotency_key=log.idempotency_key,
            delay_seconds=delay
        )
        return job_id
