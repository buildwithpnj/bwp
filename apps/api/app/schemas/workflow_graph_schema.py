from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class GraphNode(BaseModel):
    node_id: str
    workflow_run_id: str
    step_id: Optional[str] = None
    label: str
    step_type: str  # task, checkpoint, transition
    execution_status: str  # pending, executing, succeeded, failed, paused
    retry_count: int = 0
    recovery_status: str = "none"  # none, recovered, dead_lettered
    has_diagnostic_report: bool = False
    has_recovery_options: bool = False
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    duration_ms: Optional[float] = None
    approval_required: bool = False
    failure_type: Optional[str] = None
    diagnostic_details: Optional[Dict[str, Any]] = None

class GraphEdge(BaseModel):
    edge_id: str
    from_node_id: str
    to_node_id: str
    transition_type: str  # sequence, fallback, rollback
    transition_status: str  # active, completed, skipped

class WorkflowGraph(BaseModel):
    workflow_run_id: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
