import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_db, get_current_user
from app.models.user import User
from app.models.action_approval_models import ActionApprovalRequest

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.asyncio
async def test_list_approvals_admin_success(client):
    db = AsyncMock()
    
    async def override_db():
        yield db
        
    async def override_admin_user():
        return User(id="admin_123", email="admin@example.com", role="admin", password_hash="hash")
        
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_admin_user
    
    req = ActionApprovalRequest(id="apr_1", action_name="update_task", status="pending")
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = [req]
    db.execute.return_value = mock_res
    
    try:
        response = client.get("/api/governance/approvals")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "apr_1"
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

@pytest.mark.asyncio
async def test_list_approvals_normal_user_forbidden(client):
    # conftest default current user is "approved_user" (non-admin)
    response = client.get("/api/governance/approvals")
    assert response.status_code == 403
    assert "privileges" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_get_approval_metrics_admin_success(client):
    async def override_admin_user():
        return User(id="admin_123", email="admin@example.com", role="admin", password_hash="hash")
        
    app.dependency_overrides[get_current_user] = override_admin_user
    
    try:
        with patch("app.services.approval_metrics_service.ApprovalMetricsService.get_metrics", return_value={"total_requests": 10}):
            response = client.get("/api/governance/approvals/metrics")
            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 10
    finally:
        app.dependency_overrides.pop(get_current_user, None)
