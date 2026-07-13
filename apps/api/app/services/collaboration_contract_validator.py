from typing import Dict, Any

class CollaborationContractValidator:
    @classmethod
    def validate_payload(cls, sender: str, receiver: str, payload: Dict[str, Any]) -> bool:
        """
        Validates handoff payload fields based on sender and receiver agent types.
        """
        if sender == "CodeReviewerAgent" and receiver == "DatabaseAuditorAgent":
            # Must mention code analysis details
            return "code_findings" in payload or "anomaly_detected" in payload
            
        if sender == "DatabaseAuditorAgent" and receiver == "WorkflowDiagnosticianAgent":
            # Must mention lock anomalies
            return "database_locks" in payload or "schema_conflicts" in payload
            
        return True
