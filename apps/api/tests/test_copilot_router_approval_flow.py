import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_db
from app.models.copilot_session import CopilotSession
from app.services.action_policy_registry import ActionPolicyTier

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_session():
    return CopilotSession(
        id="sess_123",
        user_id="mock_session_id",
        chat_history=[],
        is_active=True
    )

@pytest.mark.asyncio
async def test_chat_auto_executes_safe_action(client, mock_session):
    db = AsyncMock()
    db.add = MagicMock()
    
    async def override_db():
        yield db
    app.dependency_overrides[get_db] = override_db

    mock_llm_res = {
        "status": "success",
        "content": "Creating a note for you. <action>{\"action_name\": \"create_note\", \"payload\": {\"title\": \"My Note\", \"content\": \"Hello world\"}}</action>"
    }
    
    try:
        with patch("app.services.copilot_router_service.LLMProviderRouter.route_completion", AsyncMock(return_value=mock_llm_res)), \
             patch("app.services.copilot_session_service.CopilotSessionService.get_or_create_session", AsyncMock(return_value=mock_session)), \
             patch("app.services.copilot_session_service.CopilotSessionService.append_message", AsyncMock(return_value=mock_session)), \
             patch("app.services.ui_action_bridge.UiActionBridge.verify_action_outcome", AsyncMock(return_value=True)):
            
            response = client.post(
                "/api/copilot/chat?query=create+a+note",
                json={
                    "current_route": "/notes",
                    "visible_module_hints": [],
                    "selected_entity_id": None,
                    "workflow_state": None
                }
            )
            assert response.status_code == 200
            data = response.json()
            
            assert data["approval_required"] is False
            assert "executed successfully" in data["reply"].lower()
            assert data["suggested_action"]["action_name"] == "create_note"
    finally:
        app.dependency_overrides.pop(get_db, None)

@pytest.mark.asyncio
async def test_chat_pauses_confirm_first_action(client, mock_session):
    db = AsyncMock()
    db.add = MagicMock()
    
    async def override_db():
        yield db
    app.dependency_overrides[get_db] = override_db

    mock_llm_res = {
        "status": "success",
        "content": "Updating the task. <action>{\"action_name\": \"update_task\", \"payload\": {\"task_id\": \"task_123\", \"status\": \"completed\"}}</action>"
    }
    
    try:
        with patch("app.services.copilot_router_service.LLMProviderRouter.route_completion", AsyncMock(return_value=mock_llm_res)), \
             patch("app.services.copilot_session_service.CopilotSessionService.get_or_create_session", AsyncMock(return_value=mock_session)), \
             patch("app.services.copilot_session_service.CopilotSessionService.append_message", AsyncMock(return_value=mock_session)):
            response = client.post(
                "/api/copilot/chat?query=complete+task",
                json={
                    "current_route": "/dashboard",
                    "visible_module_hints": [],
                    "selected_entity_id": None,
                    "workflow_state": None
                }
            )
            assert response.status_code == 200
            data = response.json()
            
            assert data["approval_required"] is True
            assert data["token"] is not None
            assert data["approval_request"]["action_name"] == "update_task"
            assert "requires approval" in data["reply"].lower()
    finally:
        app.dependency_overrides.pop(get_db, None)

@pytest.mark.asyncio
async def test_chat_blocks_admin_only_for_normal_user(client, mock_session):
    db = AsyncMock()
    db.add = MagicMock()
    
    async def override_db():
        yield db
    app.dependency_overrides[get_db] = override_db

    mock_llm_res = {
        "status": "success",
        "content": "Triggering system sync. <action>{\"action_name\": \"trigger_system_sync\", \"payload\": {}}</action>"
    }
    
    try:
        with patch("app.services.copilot_router_service.LLMProviderRouter.route_completion", AsyncMock(return_value=mock_llm_res)), \
             patch("app.services.copilot_session_service.CopilotSessionService.get_or_create_session", AsyncMock(return_value=mock_session)), \
             patch("app.services.copilot_session_service.CopilotSessionService.append_message", AsyncMock(return_value=mock_session)):
            response = client.post(
                "/api/copilot/chat?query=trigger+system+sync",
                json={
                    "current_route": "/dashboard",
                    "visible_module_hints": [],
                    "selected_entity_id": None,
                    "workflow_state": None
                }
            )
            assert response.status_code == 200
            data = response.json()
            
            assert data["approval_required"] is False
            assert "blocked" in data["reply"].lower()
            assert data["suggested_action"] is None
    finally:
        app.dependency_overrides.pop(get_db, None)
