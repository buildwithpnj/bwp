import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.workflow_execution_service import WorkflowExecutionService
from app.models.workflow_run import WorkflowRun

@pytest.mark.asyncio
async def test_workflow_pause_blocks_execution():
    db = AsyncMock()
    
    # Paused status
    wf = WorkflowRun(
        id="wf_paused",
        goal="test",
        steps=[{"action_name": "create_lesson_note", "payload": {"title": "X", "content": "Y"}}],
        current_step_index=0,
        status="paused"
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = wf
    db.execute.return_value = mock_res
    
    res = await WorkflowExecutionService.execute_current_step(db, wf, "user_123")
    assert res["status"] == "paused"
    # Should not instantiate ActionLog
    db.add.assert_not_called()
