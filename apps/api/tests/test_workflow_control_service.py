import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.workflow_control_service import WorkflowControlService
from app.schemas.workflow_control_request import WorkflowControlRequest
from app.models.workflow_run import WorkflowRun

@pytest.mark.asyncio
async def test_workflow_control_pause_and_resume():
    db = AsyncMock()
    
    wf = WorkflowRun(
        id="wf_123",
        goal="review",
        reasoning_summary="test",
        steps=[],
        status="executing"
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = wf
    db.execute.return_value = mock_res
    
    # 1. Test Pause
    req_pause = WorkflowControlRequest(control_type="pause_workflow", reason="take a break")
    with patch("app.services.realtime_event_emitter.RealTimeEventEmitter.emit_workflow_event", AsyncMock()) as mock_emit:
        res = await WorkflowControlService.apply_control(db, "wf_123", req_pause, "user_123", "approved_user")
        
        assert res.result_status == "applied"
        assert wf.status == "paused"
        mock_emit.assert_called_once()
        
    # 2. Test Resume
    req_resume = WorkflowControlRequest(control_type="resume_workflow", reason="continue")
    with patch("app.services.realtime_event_emitter.RealTimeEventEmitter.emit_workflow_event", AsyncMock()) as mock_emit2:
        with patch("app.services.workflow_execution_service.WorkflowExecutionService.execute_current_step", AsyncMock()) as mock_step:
            res = await WorkflowControlService.apply_control(db, "wf_123", req_resume, "user_123", "approved_user")
            
            assert res.result_status == "applied"
            assert wf.status == "executing"
            mock_emit2.assert_called_once()
            mock_step.assert_called_once()
