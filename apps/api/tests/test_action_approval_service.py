import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.action_approval_service import ActionApprovalService
from app.models.action_models import ActionApproval, ActionLog

@pytest.mark.asyncio
async def test_action_approval_decide():
    db = AsyncMock()
    
    # Mock return values for approval and log updates
    approval = ActionApproval(action_log_id="log_123", user_id="user_123", status="pending")
    log = ActionLog(user_id="user_123", action_name="create_followup_practice", status="pending")
    
    mock_app_res = MagicMock()
    mock_app_res.scalar_one_or_none.return_value = approval
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    db.execute.side_effect = [mock_app_res, mock_log_res]
    
    ok = await ActionApprovalService.decide_approval(db, "app_123", approve=True)
    assert ok is True
    assert approval.status == "approved"
    assert log.approval_status == "approved"
    db.commit.assert_called_once()
