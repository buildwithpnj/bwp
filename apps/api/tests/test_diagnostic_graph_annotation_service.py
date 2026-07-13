import pytest
from app.services.diagnostic_graph_annotation_service import DiagnosticGraphAnnotationService
from app.schemas.workflow_graph_schema import GraphNode
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport

def test_node_diagnostic_annotation():
    node = GraphNode(
        node_id="node_1",
        workflow_run_id="wf_1",
        label="step_1",
        step_type="task",
        execution_status="failed"
    )
    
    report = WorkflowDiagnosticReport(
        id="report_1",
        workflow_run_id="wf_1",
        diagnostic_type="execution_failure",
        severity="critical",
        likely_causes=["Cause"],
        evidence_points=["Evidence"],
        suggested_recovery_options=[{"action_type": "replay_failed_step", "description": "Replay", "risk_score": 0.1, "requires_approval": True, "admin_only": False}]
    )
    
    annotated = DiagnosticGraphAnnotationService.annotate_node(node, report)
    
    assert annotated.has_diagnostic_report is True
    assert annotated.has_recovery_options is True
    assert annotated.failure_type == "execution_failure"
    assert annotated.diagnostic_details["report_id"] == "report_1"
    assert annotated.diagnostic_details["severity"] == "critical"
