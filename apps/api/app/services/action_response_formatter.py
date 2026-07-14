from typing import Dict, Any, Optional

class ActionResponseFormatter:
    @classmethod
    def format_response(
        cls,
        status: str,
        action_name: str,
        result: str,
        scope: str = "workspace",
        next_steps: Optional[str] = None
    ) -> str:
        """
        Formats action outcomes into a standardized, professional text response.
        Ensures raw planning artifacts are completely removed.
        """
        formatted_status = status.title()
        human_action = action_name.replace("_", " ").title()
        
        lines = [
            f"Status: {formatted_status}",
            f"Action: {human_action}",
            f"Result: {result}",
            f"Scope: {scope}"
        ]
        
        if next_steps:
            lines.append(f"Next: {next_steps}")
            
        return "\n".join(lines)
