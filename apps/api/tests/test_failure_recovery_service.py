import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.failure_recovery_service import FailureRecoveryService
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus

@pytest.mark.asyncio
async def test_failure_recovery_trigger_retry():
    db = AsyncMock()
    log = ActionLog(
        user_id="user_123",
        action_name="create_followup_practice",
        retry_count=0,
        max_retries=3,
        execution_status=ActionExecutionStatus.FAILED
    )
    
    # Mock WorkerRetryScheduler.schedule_retry
    with patch("app.services.worker_retry_scheduler.WorkerRetryScheduler.schedule_retry", AsyncMock()) as mock_sched:
        recovered = await FailureRecoveryService.process_failure(db, log, Exception("Network issue"))
        
        assert recovered is True
        assert log.retry_count == 1
        assert log.execution_status == ActionExecutionStatus.QUEUED
        assert log.recovery_status == ActionRecoveryStatus.PENDING_RECOVERY
        mock_sched.assert_called_once_with(db, log)

@pytest.mark.asyncio
async def test_failure_recovery_exhausted_trigger_rollback():
    db = AsyncMock()
    log = ActionLog(
        user_id="user_123",
        action_name="create_followup_practice",
        retry_count=3, # Limit reached
        max_retries=3,
        execution_status=ActionExecutionStatus.FAILED
    )
    
    # Mock rollback handler
    with patch("app.services.partial_failure_handler.PartialFailureHandler.handle_partial_failure", AsyncMock()) as mock_partial:
        recovered = await FailureRecoveryService.process_failure(db, log, Exception("Network issue"))
        
        assert recovered is False
        assert log.execution_status == ActionExecutionStatus.PERMANENTLY_FAILED
        mock_partial.assert_called_once()
        args, kwargs = mock_partial.call_args
        assert args[0] == db
        assert args[1] == log
        assert str(args[2]) == "Network issue"
