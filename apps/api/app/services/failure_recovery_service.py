import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus
from app.services.action_retry_policy import ActionRetryPolicy
from app.services.partial_failure_handler import PartialFailureHandler
from app.services.action_observability_service import ActionObservabilityService

logger = logging.getLogger("failure_recovery")

class FailureRecoveryService:
    @classmethod
    async def process_failure(cls, db: AsyncSession, log: ActionLog, error: Exception) -> bool:
        """
        Coordinates recovery and retries on action execution failures.
        Returns:
            bool: True if recovered or retrying, False if permanently failed.
        """
        logger.warning(f"Processing failure for action={log.action_name} log={log.id}")
        
        # Check if retry is allowed
        if ActionRetryPolicy.should_retry(log.action_name, log.retry_count):
            log.retry_count += 1
            log.execution_status = ActionExecutionStatus.QUEUED
            log.recovery_status = ActionRecoveryStatus.PENDING_RECOVERY
            log.last_error = str(error)
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="action_retrying",
                user_id=log.user_id,
                action_name=log.action_name,
                action_log_id=log.id,
                extra={"retry_count": log.retry_count, "error": str(error)}
            )
            
            # Defer and schedule retry using V16 retry scheduler
            from app.services.worker_retry_scheduler import WorkerRetryScheduler
            try:
                await WorkerRetryScheduler.schedule_retry(db, log)
                return True
            except Exception as retry_err:
                # Recurse failure handling for retry exceptions
                return await cls.process_failure(db, log, retry_err)
                
        # If retries are exhausted or not allowed, trigger rollback
        log.execution_status = ActionExecutionStatus.PERMANENTLY_FAILED
        await db.commit()
        
        ActionObservabilityService.log_event(
            event_name="action_permanently_failed",
            user_id=log.user_id,
            action_name=log.action_name,
            action_log_id=log.id,
            extra={"error": str(error)}
        )
        
        # Run compensating rollback to recover partial states
        await PartialFailureHandler.handle_partial_failure(db, log, error)
        
        # Archive to DLQ
        from app.services.dead_letter_service import DeadLetterService
        await DeadLetterService.move_to_dlq(db, log, str(error))
        
        return False
