import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.action_execution_service import ActionExecutionService
from app.services.action_approval_service import ActionApprovalService
from app.models.action_models import ActionApproval, ActionLog

@pytest.mark.asyncio
async def test_async_approval_to_queue_flow():
    db = AsyncMock()
    
    # 1. Test auto-approved enqueuer routing
    with patch("app.services.idempotency_guard.IdempotencyGuard.validate_and_gate", AsyncMock(return_value=("key_auto", True))):
        with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock(return_value="job_auto")) as mock_enqueue:
            res = await ActionExecutionService.request_execution(
                db=db,
                user_id="user_123",
                user_role="approved_user",
                action_name="save_corrected_example",
                payload={"original": "me goes", "corrected": "I go", "explanation": "Grammar fix"}
            )
            
            assert res["status"] == "queued"
            assert res["job_id"] == "job_auto"
            mock_enqueue.assert_called_once()
            
    # 2. Test manual approval enqueuer routing
    approval = ActionApproval(action_log_id="log_manual", user_id="user_123", status="pending")
    log = ActionLog(user_id="user_123", action_name="create_followup_practice", status="pending")
    
    mock_app_res = MagicMock()
    mock_app_res.scalar_one_or_none.return_value = approval
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    db.execute.side_effect = [mock_app_res, mock_log_res]
    
    with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock()) as mock_enqueue_manual:
        ok = await ActionApprovalService.decide_approval(db, "app_123", approve=True)
        assert ok is True
        mock_enqueue_manual.assert_called_once()
