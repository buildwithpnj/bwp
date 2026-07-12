import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.middleware.preview_rate_limit import PreviewRateLimitMiddleware
from app.services.preview_budget_service import PreviewBudgetService

client = TestClient(app)

def test_session_creation():
    PreviewRateLimitMiddleware._rate_limits.clear()
    PreviewBudgetService.reset_daily_budget()
    response = client.post("/api/public-preview/session")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["session_id"]) > 10


def test_respond_blocked_intent():
    PreviewRateLimitMiddleware._rate_limits.clear()
    # Create session
    sess_res = client.post("/api/public-preview/session")
    session_id = sess_res.json()["session_id"]
    
    # Send unallowed intent query
    response = client.post(
        "/api/public-preview/respond",
        json={"session_id": session_id, "message": "Write a python script for my web app"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "blocked"
    assert "preview scope" in data["message"].lower()
