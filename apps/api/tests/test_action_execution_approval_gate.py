import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_db
from app.services.approval_token_service import ApprovalTokenService
from app.services.approval_request_service import ApprovalRequestService
from app.models.action_approval_models import ActionApprovalRequest
from app.models.action_models import ActionLog
from datetime import datetime, timezone, timedelta

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.asyncio
async def test_approve_action_success(client):
    db = AsyncMock()
    db.add = MagicMock()
    
    async def override_db():
        yield db
    app.dependency_overrides[get_db] = override_db

    user_id = "mock_session_id"  # aligned with override_get_current_user in conftest
    tenant_id = "tenant_session"
    
    log = ActionLog(id="act_123", user_id=user_id, tenant_id=tenant_id, action_name="update_task", status="pending")
    req = ActionApprovalRequest(
        id="apr_123",
        action_log_id="act_123",
        user_id=user_id,
        tenant_id=tenant_id,
        action_name="update_task",
        policy_tier="confirm_first",
        risk_level="medium",
        status="pending",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    
    mock_req_res = MagicMock()
    mock_req_res.scalar_one_or_none.return_value = req
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    # First query gets req, second gets log
    db.execute.side_effect = [mock_req_res, mock_log_res]
    
    token = ApprovalTokenService.generate_token(req.id, user_id, tenant_id)
    
    try:
        with patch("app.services.action_execution_service.ActionExecutionService.execute_log_action", AsyncMock(return_value={"status": "success"})), \
             patch("app.services.ui_action_bridge.UiActionBridge.verify_action_outcome", AsyncMock(return_value=True)):
            
            response = client.post(
                f"/api/copilot/approve?approval_id={req.id}",
                json={
                    "approve": True,
                    "token": token
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "executed successfully" in data["message"].lower()
            
            assert req.status == "executed"
            assert ApprovalTokenService.validate_and_burn_token(token, user_id, tenant_id) is None
    finally:
        app.dependency_overrides.pop(get_db, None)

@pytest.mark.asyncio
async def test_deny_action_prevents_execution(client):
    db = AsyncMock()
    db.add = MagicMock()
    
    async def override_db():
        yield db
    app.dependency_overrides[get_db] = override_db

    user_id = "mock_session_id"
    tenant_id = "tenant_session"
    
    log = ActionLog(id="act_123", user_id=user_id, tenant_id=tenant_id, action_name="delete_note", status="pending")
    req = ActionApprovalRequest(
        id="apr_123",
        action_log_id="act_123",
        user_id=user_id,
        tenant_id=tenant_id,
        action_name="delete_note",
        policy_tier="destructive_confirmed",
        risk_level="high",
        status="pending",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    
    mock_req_res = MagicMock()
    mock_req_res.scalar_one_or_none.return_value = req
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    db.execute.side_effect = [mock_req_res, mock_log_res]
    
    token = ApprovalTokenService.generate_token(req.id, user_id, tenant_id)
    
    try:
        with patch("app.services.action_execution_service.ActionExecutionService.execute_log_action", AsyncMock()) as mock_execute:
            
            response = client.post(
                f"/api/copilot/approve?approval_id={req.id}",
                json={
                    "approve": False,
                    "token": token
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "denied"
            assert "action denied" in data["message"].lower()
            
            mock_execute.assert_not_called()
            assert req.status == "denied"
    finally:
        app.dependency_overrides.pop(get_db, None)
