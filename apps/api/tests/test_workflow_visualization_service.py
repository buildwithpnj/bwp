import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.workflow_visualization_service import WorkflowVisualizationService
from app.models.workflow_run import WorkflowRun
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport

@pytest.mark.asyncio
async def test_workflow_visualization_graph_building():
    db = AsyncMock()
    
    wf = WorkflowRun(
        id="wf_viz_123",
        goal="test viz",
        steps=[{"action_name": "create_lesson_note", "payload": {}}],
        current_step_index=0,
        status="failed"
    )
    
    mock_wf_res = MagicMock()
    mock_wf_res.scalar_one_or_none.return_value = wf
    
    report = WorkflowDiagnosticReport(
        id="report_abc",
        workflow_run_id="wf_viz_123",
        diagnostic_type="execution_failure",
        severity="critical",
        likely_causes=["Cause"],
        evidence_points=["Evidence"],
        suggested_recovery_options=[{"action_type": "replay_failed_step", "description": "Replay", "risk_score": 0.1, "requires_approval": True, "admin_only": False}]
    )
    
    mock_diag_res = MagicMock()
    mock_diag_res.scalars.return_value.all.return_value = [report]
    
    mock_del_res = MagicMock()
    mock_del_res.scalars.return_value.all.return_value = []
    
    mock_col_res = MagicMock()
    mock_col_res.scalars.return_value.all.return_value = []
    
    mock_ing_res = MagicMock()
    mock_ing_res.scalar_one_or_none.return_value = None
    
    mock_sim_res = MagicMock()
    mock_sim_res.scalars.return_value.first.return_value = None
    
    db.execute.side_effect = [mock_wf_res, mock_diag_res, mock_del_res, mock_col_res, mock_ing_res, mock_sim_res]
    
    graph = await WorkflowVisualizationService.build_workflow_graph(db, "wf_viz_123")
    
    assert graph is not None
    assert len(graph.nodes) == 3  # Start + 1 Step + End node
    assert graph.nodes[1].has_diagnostic_report is True
    assert graph.nodes[1].diagnostic_details["report_id"] == "report_abc"
