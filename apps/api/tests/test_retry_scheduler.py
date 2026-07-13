import pytest
from unittest.mock import AsyncMock, patch
from app.services.worker_retry_scheduler import WorkerRetryScheduler
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_retry_scheduler_exponential_backoff():
    db = AsyncMock()
    log = ActionLog(
        user_id="user_123",
        action_name="create_followup_practice",
        retry_count=1,
        idempotency_key="key_retry"
    )
    
    with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock(return_value="job_abc")) as mock_enqueue:
        job_id = await WorkerRetryScheduler.schedule_retry(db, log)
        
        assert job_id == "job_abc"
        assert log.retry_scheduled_at is not None
        mock_enqueue.assert_called_once()
        args, kwargs = mock_enqueue.call_args
        assert kwargs["delay_seconds"] == 4  # 2 * (2 ** 1) = 4 seconds
