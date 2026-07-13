import logging
from typing import List, Dict, Any
from app.models.workflow_run import WorkflowRun
from app.schemas.workflow_graph_schema import GraphNode, GraphEdge

logger = logging.getLogger("graph_projection_service")

class GraphProjectionService:
    @classmethod
    def project_workflow(cls, wf: WorkflowRun) -> Dict[str, Any]:
        """
        Projects a WorkflowRun and its steps into a list of nodes and sequential transition edges.
        """
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        
        # 1. Add Start Trigger node
        start_id = f"node_{wf.id}_start"
        nodes.append(
            GraphNode(
                node_id=start_id,
                workflow_run_id=wf.id,
                label="Start Workflow Trigger",
                step_type="transition",
                execution_status="succeeded"
            )
        )
        
        prev_node_id = start_id
        
        # 2. Iterate and project workflow steps
        for idx, step in enumerate(wf.steps):
            node_id = f"node_{wf.id}_step_{idx}"
            action_name = step.get("action_name", "unknown_action")
            
            # Determine node status mapping
            status = "pending"
            if idx < wf.current_step_index:
                status = "succeeded"
            elif idx == wf.current_step_index:
                if wf.status == "failed":
                    status = "failed"
                elif wf.status == "paused":
                    status = "paused"
                elif wf.status == "paused_approval":
                    status = "paused"
                elif wf.status == "executing":
                    status = "executing"
                else:
                    status = "pending"
            else:
                status = "pending"
                
            nodes.append(
                GraphNode(
                    node_id=node_id,
                    workflow_run_id=wf.id,
                    step_id=node_id,
                    label=action_name,
                    step_type="task",
                    execution_status=status,
                    approval_required=bool(wf.requires_approval and idx == 0)
                )
            )
            
            # Create Edge from previous step node to this node
            edge_id = f"edge_{prev_node_id}_to_{node_id}"
            edges.append(
                GraphEdge(
                    edge_id=edge_id,
                    from_node_id=prev_node_id,
                    to_node_id=node_id,
                    transition_type="sequence",
                    transition_status="completed" if status in ["succeeded", "executing", "failed"] else "skipped"
                )
            )
            
            prev_node_id = node_id
            
        # 3. Add Success Finish node
        end_id = f"node_{wf.id}_end"
        end_status = "succeeded" if wf.status == "succeeded" else "pending"
        nodes.append(
            GraphNode(
                node_id=end_id,
                workflow_run_id=wf.id,
                label="Workflow Completed",
                step_type="transition",
                execution_status=end_status
            )
        )
        
        edges.append(
            GraphEdge(
                edge_id=f"edge_{prev_node_id}_to_{end_id}",
                from_node_id=prev_node_id,
                to_node_id=end_id,
                transition_type="sequence",
                transition_status="completed" if end_status == "succeeded" else "skipped"
            )
        )
        
        return {"nodes": nodes, "edges": edges}
