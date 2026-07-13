import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.dead_letter_service import DeadLetterService
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus

@pytest.mark.asyncio
async def test_dead_letter_flow():
    db = AsyncMock()
    log = ActionLog(
        user_id="user_123",
        action_name="create_followup_practice",
        status="pending",
        execution_status=ActionExecutionStatus.FAILED
    )
    
    # 1. Move to DLQ
    await DeadLetterService.move_to_dlq(db, log, "Retries exhausted")
    assert log.execution_status == ActionExecutionStatus.PERMANENTLY_FAILED
    assert log.dead_lettered_at is not None
    assert "DLQ: Retries exhausted" in log.last_error
    
    # 2. Replay from DLQ
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = log
    db.execute.return_value = mock_res
    
    with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock()) as mock_enqueue:
        success = await DeadLetterService.replay_dlq_job(db, "log_123")
        assert success is True
        assert log.dead_lettered_at is None
        assert log.execution_status == ActionExecutionStatus.QUEUED
        assert log.retry_count == 0
        mock_enqueue.assert_called_once()
