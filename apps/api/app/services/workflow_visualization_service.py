import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.workflow_run import WorkflowRun
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport
from app.schemas.workflow_graph_schema import WorkflowGraph
from app.services.graph_projection_service import GraphProjectionService
from app.services.diagnostic_graph_annotation_service import DiagnosticGraphAnnotationService

logger = logging.getLogger("workflow_visualization_service")

class WorkflowVisualizationService:
    @classmethod
    async def build_workflow_graph(
        cls,
        db: AsyncSession,
        workflow_run_id: str
    ) -> Optional[WorkflowGraph]:
        """
        Loads WorkflowRun, compiles nodes and edges, finds diagnostics, and annotates node objects.
        """
        # 1. Load WorkflowRun
        wf_stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        wf_res = await db.execute(wf_stmt)
        wf = wf_res.scalar_one_or_none()
        
        if not wf:
            logger.error(f"Cannot visualize: Workflow run {workflow_run_id} not found.")
            return None
            
        # 2. Project workflow run steps to layout nodes and edge routes
        projection = GraphProjectionService.project_workflow(wf)
        nodes = projection["nodes"]
        edges = projection["edges"]
        
        # 3. Load latest diagnostic reports
        diag_stmt = select(WorkflowDiagnosticReport).where(
            WorkflowDiagnosticReport.workflow_run_id == workflow_run_id
        ).order_by(WorkflowDiagnosticReport.created_at.desc())
        diag_res = await db.execute(diag_stmt)
        reports = diag_res.scalars().all()
        
        # 4. Overlay failure diagnostics onto nodes if any reports exist
        if reports:
            latest_report = reports[0]
            # Match report to the currently failing active step index
            failed_node_id = f"node_{wf.id}_step_{wf.current_step_index}"
            for idx, node in enumerate(nodes):
                if node.node_id == failed_node_id:
                    nodes[idx] = DiagnosticGraphAnnotationService.annotate_node(node, latest_report)
                    
        # 5. Overlay subagent delegation runs as subnodes
        from app.models.delegation_run import DelegationRun
        from app.schemas.workflow_graph_schema import GraphNode, GraphEdge
        
        del_stmt = select(DelegationRun).where(DelegationRun.workflow_run_id == workflow_run_id)
        del_res = await db.execute(del_stmt)
        delegations = del_res.scalars().all()
        
        for run in delegations:
            subnode_id = f"node_{workflow_run_id}_specialist_{run.id}"
            nodes.append(
                GraphNode(
                    node_id=subnode_id,
                    workflow_run_id=workflow_run_id,
                    label=f"Specialist: {run.specialist_type}",
                    step_type="transition",
                    execution_status="succeeded" if run.outcome_status == "succeeded" else "failed",
                    diagnostic_details={
                        "reasoning_summary": run.reasoning_summary,
                        "structured_findings": run.structured_findings,
                        "suggested_next_step": run.suggested_next_step
                    }
                )
            )
            parent_id = run.parent_step_id or f"node_{workflow_run_id}_step_0"
            edges.append(
                GraphEdge(
                    edge_id=f"edge_{parent_id}_to_{subnode_id}",
                    from_node_id=parent_id,
                    to_node_id=subnode_id,
                    transition_type="fallback",
                    transition_status="completed"
                )
            )
            
        # 6. Overlay multi-agent collaboration runs & handoffs
        from app.models.collaboration_run import CollaborationRun
        from app.models.collaboration_handoff import CollaborationHandoff
        
        col_stmt = select(CollaborationRun).where(CollaborationRun.workflow_run_id == workflow_run_id)
        col_res = await db.execute(col_stmt)
        collaborations = col_res.scalars().all()
        
        for col_run in collaborations:
            col_node_id = f"node_{workflow_run_id}_collab_{col_run.id}"
            nodes.append(
                GraphNode(
                    node_id=col_node_id,
                    workflow_run_id=workflow_run_id,
                    label=f"Collaboration: {', '.join(col_run.participating_agents)}",
                    step_type="transition",
                    execution_status=col_run.coordination_status
                )
            )
            # Edge from step 0 to collaboration node
            edges.append(
                GraphEdge(
                    edge_id=f"edge_step0_to_{col_node_id}",
                    from_node_id=f"node_{workflow_run_id}_step_0",
                    to_node_id=col_node_id,
                    transition_type="fallback",
                    transition_status="completed"
                )
            )
            
        # 7. Check if there is an ingestion source
        from app.models.multimodal_ingest_log import MultimodalIngestLog
        ing_stmt = select(MultimodalIngestLog).where(MultimodalIngestLog.workflow_run_id == workflow_run_id)
        ing_res = await db.execute(ing_stmt)
        ing_log = ing_res.scalar_one_or_none()
        
        if ing_log:
            start_node_id = f"node_{workflow_run_id}_start"
            for idx, node in enumerate(nodes):
                if node.node_id == start_node_id:
                    nodes[idx].label = f"Start Trigger (Source: {ing_log.media_type})"
                    nodes[idx].diagnostic_details = {
                        "ingested_filename": ing_log.raw_filename,
                        "ingestion_confidence": ing_log.confidence
                    }
                    
        # 8. Check for sandboxed simulation preflight results
        from app.models.simulation_run import SimulationRun
        sim_stmt = select(SimulationRun).where(SimulationRun.workflow_run_id == workflow_run_id).order_by(SimulationRun.created_at.desc())
        sim_res = await db.execute(sim_stmt)
        sim_log = sim_res.scalars().first()
        
        if sim_log:
            start_node_id = f"node_{workflow_run_id}_start"
            for idx, node in enumerate(nodes):
                if node.node_id == start_node_id:
                    if not nodes[idx].diagnostic_details:
                        nodes[idx].diagnostic_details = {}
                    nodes[idx].diagnostic_details["sandbox_preflight_score"] = sim_log.predicted_success_score
                    nodes[idx].diagnostic_details["sandbox_risk_score"] = sim_log.risk_score
                    nodes[idx].diagnostic_details["predicted_failures"] = sim_log.likely_failures
                    
        return WorkflowGraph(
            workflow_run_id=workflow_run_id,
            nodes=nodes,
            edges=edges
        )
