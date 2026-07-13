import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.local_loop_runtime import LocalLoopRuntime
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
