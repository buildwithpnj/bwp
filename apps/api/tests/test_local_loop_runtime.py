import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.local_loop_runtime import LocalLoopRuntime
from app.services.full_loop_runtime import FullLoopRuntime
from app.llm_settings import llm_settings

@pytest.mark.asyncio
async def test_execute_local_loop_success():
    # 1. Mock Planner output (JSON steps list)
    mock_planner_response = MagicMock()
    mock_planner_response.status_code = 200
    mock_planner_response.json = MagicMock(return_value={
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": '[{"step_index": 1, "tool": "search", "query_or_path": "habits routines"}, {"step_index": 2, "tool": "write_action", "query_or_path": "save_example"}]'
        },
        "done": True
    })

    # 2. Mock RAG Answer content
    mock_answer_response = MagicMock()
    mock_answer_response.status_code = 200
    mock_answer_response.json = MagicMock(return_value={
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "This is a grounded output citing habits routines."
        },
        "done": True
    })

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Side effect to handle multiple mock completion calls (Planner then Answer)
        mock_post.side_effect = [mock_planner_response, mock_answer_response]
        llm_settings.llm_provider = "ollama"

        result = await LocalLoopRuntime.execute_local_loop(
            prompt="sync habits routines",
            max_steps=3
        )

        assert result["status"] == "success"
        assert len(result["steps"]) == 2
        # Check safety check: write action is blocked/mocked
        assert result["executed_steps"][1]["tool"] == "write_action"
        assert result["executed_steps"][1]["status"] == "mocked_disabled_locally"
        assert "Blocked" in result["executed_steps"][1]["result"] or "blocked" in result["executed_steps"][1]["result"].lower()
        assert result["grounded"] is True

@pytest.mark.asyncio
async def test_execute_local_loop_tenant_block():
    # Verify tenant isolation limits block unauthorized requests
    original_val = llm_settings.tenant_guards_enabled
    llm_settings.tenant_guards_enabled = True
    try:
        res = FullLoopRuntime.execute_full_run(
            prompt="read config files",
            tenant_id="blocked_tenant"
        )
        assert res["status"] == "failed"
        assert res["stop_reason"] == "stop_tenant_guard"
        assert "Access Denied" in res["final_answer"]
    finally:
        llm_settings.tenant_guards_enabled = original_val

@pytest.mark.asyncio
async def test_execute_local_loop_no_progress_halt():
    # Verify duplicate consecutive search queries trigger no-progress stops
    original_val = llm_settings.no_progress_stop_enabled
    llm_settings.no_progress_stop_enabled = True
    try:
        from app.services.loop_state_store import LoopStateStore
        state_id = LoopStateStore.initialize_state("sync data", "tenant_1")
        
        # Simulate consecutive duplicate steps
        LoopStateStore.append_step(state_id, {"step_index": 1, "tool": "search", "query_or_path": "sync configuration settings"})
        LoopStateStore.append_step(state_id, {"step_index": 2, "tool": "search", "query_or_path": "sync configuration settings"})
        
        from app.services.loop_decision_service import LoopDecisionService
        outcome = LoopDecisionService.evaluate_outcome(state_id)
        assert outcome == "stop_no_progress"
    finally:
        llm_settings.no_progress_stop_enabled = original_val

@pytest.mark.asyncio
async def test_execute_local_loop_confidence_collapse_halt():
    # Verify confidence metrics collapses trigger stops
    original_val = llm_settings.confidence_collapse_protection
    llm_settings.confidence_collapse_protection = True
    try:
        from app.services.loop_state_store import LoopStateStore
        state_id = LoopStateStore.initialize_state("read logs", "tenant_1")
        LoopStateStore.append_step(state_id, {"step_index": 1, "tool": "search", "query_or_path": "read logs"})
        
        # Simulate confidence score drop
        state = LoopStateStore.get_state(state_id)
        state["confidence"] = 0.3
        
        from app.services.loop_decision_service import LoopDecisionService
        outcome = LoopDecisionService.evaluate_outcome(state_id)
        assert outcome == "stop_confidence_collapse"
    finally:
        llm_settings.confidence_collapse_protection = original_val

@pytest.mark.asyncio
async def test_execute_local_loop_provider_fallback():
    # Verify provider fallback routes to cloud mock when Ollama is unreachable
    original_provider = llm_settings.llm_provider
    original_fallback = llm_settings.provider_fallback_enabled
    llm_settings.llm_provider = "ollama"
    llm_settings.provider_fallback_enabled = True
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Simulate timeout connection failure
        mock_post.side_effect = Exception("Connection Refused")
        
        from app.services.llm_provider_router import LLMProviderRouter
        res = await LLMProviderRouter.route_completion(
            messages=[{"role": "user", "content": "sync settings"}],
            json_mode=True
        )
        assert res["provider"] == "cloud_fallback"
        assert res["status"] == "success"
        assert "Cloud fallback response" in res["content"]
        
    llm_settings.llm_provider = original_provider
    llm_settings.provider_fallback_enabled = original_fallback
