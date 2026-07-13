import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus
from app.services.action_execution_service import ActionExecutionService
from app.services.idempotency_guard import IdempotencyGuard, DuplicateRequestException
from app.services.action_dispatcher import ActionDispatcher
from app.services.action_observability_service import ActionObservabilityService
from app.services.failure_recovery_service import FailureRecoveryService

logger = logging.getLogger("action_worker")

class ActionWorker:
    @classmethod
    async def process_one_job(cls, db: AsyncSession, queue_name: str = "actions") -> bool:
        """
        Pulls a single job from the queue and executes it.
        Returns:
            bool: True if a job was processed, False if queue was empty.
        """
        adapter = ActionDispatcher.get_adapter()
        job = await adapter.dequeue(queue_name)
        if not job:
            return False
            
        logger.info(f"Worker picked up job_id={job.job_id} for action={job.action_name}")
        
        # Load ActionLog
        stmt = select(ActionLog).where(ActionLog.id == job.action_log_id)
        res = await db.execute(stmt)
        log = res.scalar_one_or_none()
        
        if not log:
            logger.error(f"ActionLog not found for log_id={job.action_log_id}")
            return True
            
        # Validate lifecycle state: only approved/queued can execute
        if log.execution_status not in [ActionExecutionStatus.APPROVED, ActionExecutionStatus.QUEUED, ActionExecutionStatus.SUGGESTED]:
            logger.warning(f"Invalid lifecycle transition: log {log.id} status is {log.execution_status}")
            return True
            
        # Re-check Idempotency before execution
        if log.idempotency_key:
            # Check if there is another SUCCEEDED action log with the same key
            dup_stmt = select(ActionLog).where(
                ActionLog.idempotency_key == log.idempotency_key,
                ActionLog.execution_status == ActionExecutionStatus.SUCCEEDED,
                ActionLog.id != log.id
            )
            dup_res = await db.execute(dup_stmt)
            if dup_res.scalars().all():
                log.execution_status = ActionExecutionStatus.FAILED
                log.last_error = "Idempotency Gate: Action already succeeded in another thread."
                await db.commit()
                
                ActionObservabilityService.log_event(
                    event_name="action_duplicate_blocked",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id,
                    extra={"worker_id": "memory_worker", "job_id": job.job_id}
                )
                return True

        # Update log metadata
        log.queued_job_id = job.job_id
        log.queue_name = queue_name
        log.worker_id = "memory_worker"
        log.execution_source = "worker"
        await db.commit()

        # Execute using ActionExecutionService
        try:
            await ActionExecutionService.execute_log_action(db, log)
        except Exception as e:
            # execute_log_action catches errors and delegates to FailureRecoveryService,
            # but we catch any secondary thread errors here
            logger.exception(f"Unhandled worker error during execution for job {job.job_id}")
            
        return True
