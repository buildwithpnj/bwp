import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.workflow_execution_service import WorkflowExecutionService
from app.services.workflow_state_manager import WorkflowStateManager
from app.models.workflow_run import WorkflowRun

@pytest.mark.asyncio
async def test_workflow_approval_pause_and_resume():
    db = AsyncMock()
    
    # Plan has requires_approval = True
    steps = [
        {"action_name": "build_practice_plan", "payload": {"focus_area": "grammar", "num_tasks": 3}}
    ]
    
    wf = WorkflowRun(
        goal="practice plan creation",
        reasoning_summary="test",
        steps=steps,
        current_step_index=0,
        status="pending",
        requires_approval=True
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = wf
    db.execute.return_value = mock_res
    
    # 1. Start execution -> should pause
    res = await WorkflowExecutionService.start_workflow(db, "wf_123", "user_123")
    assert res["status"] == "paused_approval"
    assert wf.status == "paused_approval"
    
    # 2. Approve and resume -> should execute
    with patch("app.services.action_execution_service.ActionExecutionService.execute_log_action", AsyncMock(return_value={"status": "success"})):
        resume_res = await WorkflowStateManager.approve_and_resume(db, "wf_123", "user_123")
        assert resume_res["status"] == "succeeded"
        assert wf.status == "succeeded"
        assert wf.current_step_index == 1
