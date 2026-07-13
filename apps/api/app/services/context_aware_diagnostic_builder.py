from typing import List, Dict, Any
from app.models.action_models import ActionLog

class ContextAwareDiagnosticBuilder:
    @classmethod
    def compile_diagnostics(cls, log: ActionLog, patterns: List[str]) -> Dict[str, Any]:
        """
        Synthesizes causes and gathers evidence points from failure logs.
        """
        causes = []
        evidence = []
        severity = "warning"
        
        err_msg = log.error_message or "Unknown execution exception."
        evidence.append(f"Action Log ID: {log.id}")
        evidence.append(f"Error Message: {err_msg}")
        
        # Heuristics checking
        err_msg_lower = err_msg.lower()
        last_err_lower = (log.last_error or "").lower()
        
        if "mock" in err_msg_lower or "connection" in err_msg_lower or "dial" in err_msg_lower or "offline" in err_msg_lower:
            causes.append("Docker database services or external network dependencies are currently down on host machine.")
            severity = "critical"
        if "validation" in err_msg_lower:
            causes.append("Input payload parameter types or names do not match registry schema specifications.")
            severity = "warning"
        if "duplicate" in err_msg_lower or "idempotency" in last_err_lower:
            causes.append("Action dispatcher intercepted duplicate requests with identical payload hash keys.")
            severity = "info"
            
        if "repeated_retry_pattern" in patterns:
            causes.append("Action execution repeatedly failed and exceeded safe recovery retry thresholds.")
            severity = "critical"
            evidence.append(f"Retry Counter: {log.retry_count} of {log.max_retries}")
            
        if not causes:
            causes.append("An unhandled runtime python crash occurred during tool execution.")
            
        return {
            "severity": severity,
            "likely_causes": causes,
            "evidence_points": evidence
        }
