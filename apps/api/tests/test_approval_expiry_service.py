import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone, timedelta
from app.services.approval_expiry_service import ApprovalExpiryService
from app.models.action_approval_models import ActionApprovalRequest
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_expire_pending_requests():
    db = AsyncMock()
    
    # Create an expired request and a non-expired request
    expired_req = ActionApprovalRequest(
        id="apr_expired",
        action_log_id="act_expired",
        status="pending",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)
    )
    
    # Mock search query for expired requests
    mock_expired_res = MagicMock()
    mock_expired_res.scalars.return_value.all.return_value = [expired_req]
    
    # Mock log lookup
    log = ActionLog(id="act_expired", status="pending")
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    db.execute.side_effect = [mock_expired_res, mock_log_res]
    
    expired_count = await ApprovalExpiryService.expire_pending_requests(db)
    
    assert expired_count == 1
    assert expired_req.status == "expired"
    assert log.status == "failed"
    assert "expired" in log.error_message.lower()
    
    db.commit.assert_called_once()
