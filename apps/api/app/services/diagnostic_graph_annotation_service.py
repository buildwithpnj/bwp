import logging
from app.schemas.workflow_graph_schema import GraphNode
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport

logger = logging.getLogger("diagnostic_graph_annotation_service")

class DiagnosticGraphAnnotationService:
    @classmethod
    def annotate_node(cls, node: GraphNode, report: WorkflowDiagnosticReport) -> GraphNode:
        """
        Enriches a failed node with diagnostic cause analysis, evidence timeline, and ranked recovery options.
        """
        node.has_diagnostic_report = True
        node.has_recovery_options = len(report.suggested_recovery_options) > 0
        node.failure_type = report.diagnostic_type
        
        node.diagnostic_details = {
            "report_id": report.id,
            "severity": report.severity,
            "likely_causes": report.likely_causes,
            "evidence_points": report.evidence_points,
            "suggested_recovery_options": report.suggested_recovery_options,
            "confidence_score": report.confidence_score
        }
        
        logger.info(f"Node {node.node_id} annotated with diagnostic report {report.id}")
        return node
