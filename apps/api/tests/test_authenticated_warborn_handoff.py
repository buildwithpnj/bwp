import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_current_user

client = TestClient(app)

def test_chat_unauthenticated_rejects():
    # Remove the global override to let normal auth failure occur
    orig_override = app.dependency_overrides.pop(get_current_user, None)
    try:
        response = client.post(
            "/api/warborn/chat",
            json={"message": "hello", "session_id": "test_auth_sess"}
        )
        assert response.status_code == 401
    finally:
        if orig_override is not None:
            app.dependency_overrides[get_current_user] = orig_override
