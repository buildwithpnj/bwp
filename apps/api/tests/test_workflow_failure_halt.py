import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.workflow_execution_service import WorkflowExecutionService
from app.models.workflow_run import WorkflowRun

@pytest.mark.asyncio
async def test_workflow_failure_halts_and_rolls_back():
    db = AsyncMock()
    
    steps = [
        {"action_name": "generate_weekly_review", "payload": {"week_offset": 0}},
        {"action_name": "create_summary_note", "payload": {"topic": "Review", "notes": "Compiling results"}}
    ]
    
    wf = WorkflowRun(
        goal="review",
        reasoning_summary="test",
        steps=steps,
        current_step_index=0,
        status="pending",
        requires_approval=False
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = wf
    db.execute.return_value = mock_res
    
    # Mock ActionExecutionService.execute_log_action to return failure on step 1
    with patch("app.services.action_execution_service.ActionExecutionService.execute_log_action", AsyncMock(return_value={"status": "failed", "error": "Internal executor crash"})):
        with patch("app.services.workflow_execution_service.WorkflowExecutionService.rollback_workflow", AsyncMock()) as mock_rollback:
            res = await WorkflowExecutionService.start_workflow(db, "wf_123", "user_123")
            
            assert res["status"] == "failed"
            assert wf.status == "failed"
            assert wf.current_step_index == 0
            mock_rollback.assert_called_once_with(db, wf, "user_123")
