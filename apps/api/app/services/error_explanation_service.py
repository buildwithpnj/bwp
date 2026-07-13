from typing import Dict, Any

class ErrorExplanationService:
    @classmethod
    def explain_error(cls, error_type: str, context: Dict[str, Any]) -> str:
        """
        Translates raw execution errors into actionable, professional explanations.
        """
        mapping = {
            "validation_error": "The action payload does not conform to the required contract schema.",
            "integrity_error": "Database integrity constraint violated. This record may already exist.",
            "unauthorized": "Your authenticated user role does not possess the permissions required to run this action.",
            "timeout": "The database transaction timed out while waiting for execution.",
            "tenant_mismatch": "Action execution rejected. Cross-tenant write operations are strictly restricted."
        }
        return mapping.get(error_type, f"An unexpected error occurred during execution: {error_type}")
