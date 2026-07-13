from fastapi import APIRouter, HTTPException, Depends, status
from app.deps import CurrentUser, DB
from app.schemas.workflow_graph_schema import WorkflowGraph
from app.services.workflow_visualization_service import WorkflowVisualizationService

router = APIRouter(prefix="/api/workflows", tags=["Workflow Step Graph Visualizer"])

@router.get("/{workflow_id}/graph", response_model=WorkflowGraph, status_code=status.HTTP_200_OK)
async def get_workflow_step_graph(
    workflow_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Constructs and returns the complete layout graph representation (nodes & edges)
    for the requested workflow run, overlaying diagnostics on failed nodes.
    """
    graph = await WorkflowVisualizationService.build_workflow_graph(db, workflow_id)
    if not graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found."
        )
    return graph
