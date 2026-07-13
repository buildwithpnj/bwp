import pytest
from unittest.mock import AsyncMock, patch
from app.services.copilot_router_service import CopilotRouterService
from app.schemas.copilot_context_payload import CopilotContextPayload

@pytest.mark.asyncio
async def test_process_query_cleanses_create_task_payload():
    # Setup context
    ctx = CopilotContextPayload(current_route="/dashboard")
    
    # Mock LLM route completion to return action block with non-conforming keys
    mock_llm_result = {
        "status": "success",
        "content": 'Here is your task.\n<action>{"action_name": "create_task", "payload": {"title": "Quit Alcohol", "due_date": "2023-12-31", "notes": "Attend support groups weekly"}}</action>'
    }
    
    with patch("app.services.llm_provider_router.LLMProviderRouter.route_completion", AsyncMock(return_value=mock_llm_result)):
        db = AsyncMock()
        reply_text, action = await CopilotRouterService.process_query(db, "add a task for quit alcohol", ctx, "user_123")
        
        # Verify action tags were parsed, cleansed, and stripped from reply_text
        assert action is not None
        assert action["action_name"] == "create_task"
        # "notes" must be mapped to "description"
        assert action["payload"]["description"] == "Attend support groups weekly"
        # "due_date" must be stripped out since it is not in the schema
        assert "due_date" not in action["payload"]
        assert "<action>" not in reply_text

@pytest.mark.asyncio
async def test_process_query_fallback_heuristics_for_tasks():
    # Setup context
    ctx = CopilotContextPayload(current_route="/dashboard")
    
    # Mock LLM route completion to return reply text WITHOUT action block
    mock_llm_result = {
        "status": "success",
        "content": 'I can help you add a task for quitting alcohol.'
    }
    
    with patch("app.services.llm_provider_router.LLMProviderRouter.route_completion", AsyncMock(return_value=mock_llm_result)):
        db = AsyncMock()
        # Call query which has "add" + "task" keywords
        reply_text, action = await CopilotRouterService.process_query(db, "add a task to quit alcohol", ctx, "user_123")
        
        # Verify fallback heuristics extracted the task action
        assert action is not None
        assert action["action_name"] == "create_task"
        assert action["payload"]["title"] == "Quit alcohol"
        assert action["payload"]["category"] == "recovery"
