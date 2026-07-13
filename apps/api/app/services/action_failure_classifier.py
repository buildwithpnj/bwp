from typing import Dict, Any, Union

class ActionFailureClassifier:
    @classmethod
    def classify(cls, error: Union[Exception, str]) -> Dict[str, str]:
        """Classifies a runtime exception or error string into a structured V15 failure type."""
        err_msg = str(error)
        err_lower = err_msg.lower()
        
        error_type = "execution_exception"
        user_message = "An error occurred during action execution."
        diagnostic_message = err_msg

        if "validation" in err_lower or "schema" in err_lower or "invalid input" in err_lower:
            error_type = "validation_failure"
            user_message = "The input provided for the action is invalid."
        elif "permission" in err_lower or "unauthorized" in err_lower or "restricted" in err_lower:
            error_type = "permission_failure"
            user_message = "You do not have permission to execute this action."
        elif "approval" in err_lower:
            error_type = "approval_missing"
            user_message = "This action requires approval before execution."
        elif "duplicate" in err_lower or "already completed" in err_lower or "in progress" in err_lower:
            error_type = "duplicate_blocked"
            user_message = "This action has already been executed or is in progress."
        elif "disabled" in err_lower or "not found" in err_lower:
            error_type = "tool_disabled"
            user_message = "This tool is currently disabled or unavailable."
        elif "timeout" in err_lower:
            error_type = "timeout_failure"
            user_message = "The action timed out during execution."
        elif "database" in err_lower or "persistence" in err_lower or "integrityerror" in err_lower:
            error_type = "persistence_failure"
            user_message = "A database integrity error prevented execution."
        elif "partial" in err_lower or "rollback" in err_lower:
            error_type = "partial_side_effect_failure"
            user_message = "The action partially failed. Compacting rollbacks initiated."
        elif "recovery" in err_lower:
            error_type = "recovery_failure"
            user_message = "System recovery failed for this action."

        return {
            "error_type": error_type,
            "user_message": user_message,
            "diagnostic_message": diagnostic_message
        }
