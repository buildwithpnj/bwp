import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.action_execution_service import ActionExecutionService
from app.services.action_approval_service import ActionApprovalService
from app.models.action_models import ActionLog, ActionApproval
from app.models.action_execution_state import ActionExecutionStatus

@pytest.mark.asyncio
async def test_lifecycle_timestamps_auto_approved():
    db = AsyncMock()
    async def mock_refresh(obj):
        obj.id = "log_123"
    db.refresh = mock_refresh
    
    with patch("app.services.idempotency_guard.IdempotencyGuard.validate_and_gate", AsyncMock(return_value=("key_123", True))):
        with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock(return_value="job_123")):
            # We run update_preference action which requires no approval
            res = await ActionExecutionService.request_execution(
                db=db,
                user_id="user_123",
                user_role="approved_user",
                action_name="update_preference",
                payload={"tone": "casual", "explanation_style": "simple"}
            )
        
        # Check that we committed at various states
        db.commit.assert_called()
        
        # Capture the action log object that was added to db
        added_objects = [call[0][0] for call in db.add.call_args_list]
        log = next(obj for obj in added_objects if isinstance(obj, ActionLog))
        
        # Verify transition columns are populated
        assert log.suggested_at is not None
        assert log.approved_at is not None
        assert log.queued_at is not None
        assert log.execution_status == ActionExecutionStatus.QUEUED

@pytest.mark.asyncio
async def test_lifecycle_timestamps_manual_approval():
    db = AsyncMock()
    
    # Mocking select returns for Approval flow
    approval = ActionApproval(id="app_123", action_log_id="log_123", status="pending")
    log = ActionLog(
        id="log_123",
        user_id="user_123",
        action_name="create_followup_practice",
        execution_status=ActionExecutionStatus.PENDING_APPROVAL
    )
    
    mock_app_res = MagicMock()
    mock_app_res.scalar_one_or_none.return_value = approval
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    db.execute.side_effect = [mock_app_res, mock_log_res]
    
    with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock()) as mock_enqueue:
        ok = await ActionApprovalService.decide_approval(db, "app_123", approve=True)
        
        assert ok is True
        assert approval.status == "approved"
        assert log.approval_status == "approved"
        assert log.approved_at is not None
        assert log.execution_status == ActionExecutionStatus.QUEUED
        mock_enqueue.assert_called_once_with(
            action_log_id=log.id,
            action_name=log.action_name,
            user_id=log.user_id,
            idempotency_key=log.idempotency_key
        )
