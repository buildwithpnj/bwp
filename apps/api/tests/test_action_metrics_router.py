import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.user import User

client = TestClient(app)

from app.deps import get_current_user

def test_metrics_router_restricted():
    regular_user = User(id="user_123", email="user@example.com", role="approved_user")
    app.dependency_overrides[get_current_user] = lambda: regular_user
    try:
        response = client.get("/api/actions/metrics", headers={"Authorization": "Bearer token"})
        assert response.status_code == 403
        assert "restricted to admin" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_metrics_router_allowed():
    admin_user = User(id="admin_123", email="admin@example.com", role="internal_admin")
    app.dependency_overrides[get_current_user] = lambda: admin_user
    try:
        response = client.get("/api/actions/metrics", headers={"Authorization": "Bearer token"})
        assert response.status_code == 200
        data = response.json()
        assert "counters" in data
        assert "rates" in data
    finally:
        app.dependency_overrides.clear()
