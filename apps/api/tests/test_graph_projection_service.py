import pytest
from app.services.graph_projection_service import GraphProjectionService
from app.models.workflow_run import WorkflowRun

def test_graph_projection_node_mapping():
    wf = WorkflowRun(
        id="wf_proj_123",
        steps=[{"action_name": "create_lesson_note", "payload": {}}],
        current_step_index=0,
        status="executing",
        requires_approval=True
    )
    
    projection = GraphProjectionService.project_workflow(wf)
    nodes = projection["nodes"]
    edges = projection["edges"]
    
    assert len(nodes) == 3
    assert len(edges) == 2
    
    assert nodes[0].label == "Start Workflow Trigger"
    assert nodes[1].label == "create_lesson_note"
    assert nodes[1].execution_status == "executing"
    assert nodes[1].approval_required is True
    assert nodes[2].label == "Workflow Completed"
    assert nodes[2].execution_status == "pending"
