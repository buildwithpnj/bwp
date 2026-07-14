from typing import Dict, Any
from app.services.action_response_formatter import ActionResponseFormatter

class PermissionDenialService:
    @classmethod
    def handle_denial(
        cls, 
        action_name: str, 
        reason: str = "This request is blocked by policy."
    ) -> str:
        """
        Formats a professional, structured policy warning for blocked operations.
        """
        return ActionResponseFormatter.format_response(
            status="blocked",
            action_name=action_name,
            result=reason
        )
