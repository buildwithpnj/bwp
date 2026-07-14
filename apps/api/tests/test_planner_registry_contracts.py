import pytest
from app.services.copilot_router_service import CopilotRouterService
from app.services.copilot_action_registry import CopilotActionRegistry
from app.schemas.copilot_context_payload import CopilotContextPayload

@pytest.mark.asyncio
async def test_registry_contract_fields():
    # Verify every registered action contains the full contract fields
    for action_name in CopilotActionRegistry.list_actions():
        meta = CopilotActionRegistry.get_action(action_name)
        assert meta is not None
        assert "canonical_action_name" in meta
        assert "description" in meta
        assert "pydantic_schema" in meta
        assert "policy_tier" in meta
        assert "idempotency_strategy" in meta
        assert "verifier_class" in meta
        assert "ui_success_message" in meta
        assert "ui_failure_message" in meta

@pytest.mark.asyncio
async def test_planner_hard_rule_invent_action_blocks():
    # Hard Rule 1: Never invent an action not present in CopilotActionRegistry
    ctx = CopilotContextPayload(current_route="/dashboard")
    # Mock LLM response returning an invented action name
    mock_reply = """Some message. <action>{"action_name": "invented_unregistered_action", "payload": {}, "confidence": 1.0}</action>"""
    
    # We will patch route_completion to return this reply
    from unittest.mock import AsyncMock, patch
    with patch("app.services.llm_provider_router.LLMProviderRouter.route_completion", AsyncMock(return_value={"status": "success", "content": mock_reply})):
        reply, suggested = await CopilotRouterService.process_query(
            db=None,
            query="run fake action",
            ctx=ctx,
            user_id="user_123"
        )
    
    assert suggested == {}
    assert "I cannot execute that action" in reply
    assert "Action not present in registry" in reply

@pytest.mark.asyncio
async def test_planner_hard_rule_parameter_clarification():
    # Hard Rule 3: If required parameters are missing, ask clarification instead of guessing
    ctx = CopilotContextPayload(current_route="/dashboard")
    # update_note requires note_id; omit note_id parameter
    mock_reply = """<action>{"action_name": "update_note", "payload": {"title": "Updated Title"}, "confidence": 1.0}</action>"""
    
    from unittest.mock import AsyncMock, patch
    with patch("app.services.llm_provider_router.LLMProviderRouter.route_completion", AsyncMock(return_value={"status": "success", "content": mock_reply})):
        reply, suggested = await CopilotRouterService.process_query(
            db=None,
            query="update a note",
            ctx=ctx,
            user_id="user_123"
        )
    
    assert suggested == {}
    assert "Please specify the missing parameters for update_note." in reply

@pytest.mark.asyncio
async def test_planner_hard_rule_low_confidence_blocks():
    # Hard Rule 4: If confidence is below threshold, do not execute
    ctx = CopilotContextPayload(current_route="/dashboard")
    # Confidence 0.4 is below 0.6 threshold
    mock_reply = """<action>{"action_name": "create_note", "payload": {"title": "Title", "content": "Text"}, "confidence": 0.4}</action>"""
    
    from unittest.mock import AsyncMock, patch
    with patch("app.services.llm_provider_router.LLMProviderRouter.route_completion", AsyncMock(return_value={"status": "success", "content": mock_reply})):
        reply, suggested = await CopilotRouterService.process_query(
            db=None,
            query="create note maybe?",
            ctx=ctx,
            user_id="user_123"
        )
    
    assert suggested == {}
    assert "I cannot execute that action: Confidence below threshold." in reply
