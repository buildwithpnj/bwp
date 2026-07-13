import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus
from app.services.action_rollback_service import ActionRollbackService
from app.services.action_observability_service import ActionObservabilityService

logger = logging.getLogger("partial_failure_handler")

class PartialFailureHandler:
    @classmethod
    async def handle_partial_failure(cls, db: AsyncSession, log: ActionLog, error: Exception) -> None:
        """
        Detects partial execution failures and initiates compensating actions.
        """
        logger.error(f"Partial failure detected for action={log.action_name} id={log.id}: {str(error)}")
        
        # Mark as executing status failed and pending recovery
        log.execution_status = ActionExecutionStatus.FAILED
        log.recovery_status = ActionRecoveryStatus.PENDING_RECOVERY
        log.last_error = f"Partial Failure: {str(error)}"
        await db.commit()

        ActionObservabilityService.log_event(
            event_name="action_partial_failure",
            user_id=log.user_id,
            action_name=log.action_name,
            action_log_id=log.id,
            extra={"error": str(error)}
        )

        # Trigger compensating rollback actions
        success = await ActionRollbackService.rollback(db, log)
        if success:
            logger.info(f"Partial failure recovered successfully via rollback for action={log.id}")
        else:
            logger.error(f"Partial failure rollback FAILED for action={log.id}")
