import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.approval_request_service import ApprovalRequestService
from app.services.action_policy_registry import ActionPolicyTier
from app.models.action_approval_models import ActionApprovalRequest
from datetime import datetime, timezone, timedelta

@pytest.mark.asyncio
async def test_create_approval_request():
    db = AsyncMock()
    db.add = MagicMock()  # Synchronous mock to prevent coroutine warning
    
    req = await ApprovalRequestService.create_request(
        db=db,
        user_id="user_123",
        action_name="update_task",
        payload={"task_id": "task_1", "status": "completed"},
        tenant_id="tenant_123"
    )
    
    assert req.user_id == "user_123"
    assert req.action_name == "update_task"
    assert req.tenant_id == "tenant_123"
    assert req.policy_tier == ActionPolicyTier.CONFIRM_FIRST.value
    assert req.risk_level == "medium"
    assert req.target_type == "task"
    assert req.target_id == "task_1"
    assert req.status == "pending"
    db.add.assert_called_once()
    db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_get_and_update_approval_request():
    db = AsyncMock()
    db.add = MagicMock()
    
    # expires_at set in the future so request remains pending during the test
    future_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
    req = ActionApprovalRequest(
        id="apr_test",
        user_id="user_123",
        action_name="delete_note",
        policy_tier=ActionPolicyTier.DESTRUCTIVE_CONFIRMED.value,
        risk_level="high",
        status="pending",
        expires_at=future_expiry
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = req
    db.execute.return_value = mock_res
    
    # Get request
    found = await ApprovalRequestService.get_request(db, "apr_test")
    assert found == req
    
    # Update status to approved
    ok = await ApprovalRequestService.update_status(db, "apr_test", "approved", actor_id="actor_abc")
    assert ok is True
    assert req.status == "approved"
    assert req.approved_by == "actor_abc"
    db.commit.assert_called()
