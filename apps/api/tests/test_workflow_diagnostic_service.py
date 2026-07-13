import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.workflow_diagnostic_service import WorkflowDiagnosticService
from app.models.workflow_run import WorkflowRun
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_generate_diagnostic_report_for_failed_run():
    db = AsyncMock()
    
    wf = WorkflowRun(
        id="wf_diag_123",
        goal="test diagnostics",
        steps=[{"action_name": "create_lesson_note", "payload": {}}],
        current_step_index=0,
        status="failed"
    )
    
    mock_wf_res = MagicMock()
    mock_wf_res.scalar_one_or_none.return_value = wf
    
    log = ActionLog(
        id="log_fail_456",
        user_id="user_123",
        action_name="create_lesson_note",
        status="failed",
        error_message="Connection refused",
        retry_count=0
    )
    
    mock_log_res = MagicMock()
    mock_log_res.scalar_one_or_none.return_value = log
    
    # Mock database queries
    db.execute.side_effect = [mock_wf_res, mock_log_res]
    
    report = await WorkflowDiagnosticService.generate_report(db, "wf_diag_123", "log_fail_456")
    
    assert report is not None
    assert report.workflow_run_id == "wf_diag_123"
    assert report.action_log_id == "log_fail_456"
    assert "Docker database services" in report.likely_causes[0]
    assert len(report.suggested_recovery_options) > 0
    assert report.suggested_recovery_options[0]["action_type"] == "replay_failed_step"
