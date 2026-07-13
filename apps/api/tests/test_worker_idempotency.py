import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.workers.action_worker import ActionWorker
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus
from app.services.action_dispatcher import ActionDispatcher
from app.services.queue_adapter import MemoryQueueAdapter, QueueJob

@pytest.mark.asyncio
async def test_worker_idempotency_gate():
    db = AsyncMock()
    
    # Mock log has key_123
    log = ActionLog(
        id="log_duplicate",
        user_id="user_123",
        action_name="update_preference",
        status="pending",
        execution_status=ActionExecutionStatus.QUEUED,
        idempotency_key="key_123"
    )
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    # Mock database to return the duplicate action log first, then return an existing SUCCEEDED action log
    existing_succeeded_log = ActionLog(
        id="log_original",
        user_id="user_123",
        action_name="update_preference",
        execution_status=ActionExecutionStatus.SUGGESTED
    )
    
    mock_dup_res = MagicMock()
    mock_dup_res.scalars.return_value.all.return_value = [existing_succeeded_log]
    
    db.execute.side_effect = [mock_log_res, mock_dup_res]
    
    # Enqueue a job
    adapter = MemoryQueueAdapter()
    await adapter.clear("actions")
    ActionDispatcher.set_adapter(adapter)
    
    job = QueueJob(
        action_log_id="log_duplicate",
        action_name="update_preference",
        user_id="user_123",
        idempotency_key="key_123",
        metadata={"queue_name": "actions"}
    )
    await adapter.enqueue(job)
    
    with patch("app.services.action_execution_service.ActionExecutionService.execute_log_action", AsyncMock()) as mock_exec:
        processed = await ActionWorker.process_one_job(db, "actions")
        assert processed is True
        # execute_log_action should NOT be called since the idempotency check fails
        mock_exec.assert_not_called()
        assert log.execution_status == ActionExecutionStatus.FAILED
        assert "already succeeded" in log.last_error
