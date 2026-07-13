import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.workflow_control_service import WorkflowControlService
from app.schemas.workflow_control_request import WorkflowControlRequest
from app.models.workflow_run import WorkflowRun

@pytest.mark.asyncio
async def test_workflow_cancel_and_rollback():
    db = AsyncMock()
    
    wf = WorkflowRun(
        id="wf_cancel",
        goal="test",
        steps=[],
        status="executing"
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = wf
    db.execute.return_value = mock_res
    
    req = WorkflowControlRequest(control_type="cancel_workflow", reason="stop")
    with patch("app.services.realtime_event_emitter.RealTimeEventEmitter.emit_workflow_event", AsyncMock()) as mock_emit:
        with patch("app.services.workflow_execution_service.WorkflowExecutionService.rollback_workflow", AsyncMock()) as mock_rollback:
            res = await WorkflowControlService.apply_control(db, "wf_cancel", req, "user_123", "approved_user")
            
            assert res.result_status == "applied"
            assert wf.status == "cancelled"
            mock_emit.assert_called_once()
            mock_rollback.assert_called_once_with(db, wf, "user_123")
