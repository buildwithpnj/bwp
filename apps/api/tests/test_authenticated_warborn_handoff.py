import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_unauthenticated_rejects():
    response = client.post(
        "/api/warborn/chat",
        json={"message": "hello", "session_id": "test_auth_sess"}
    )
    # Rejects unauthorized
    assert response.status_code == 401
