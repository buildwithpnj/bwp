from typing import Dict, Any

class UserFacingOutcomeRenderer:
    @classmethod
    def render_outcome(cls, outcome: str, action_name: str, details: Dict[str, Any]) -> str:
        """
        Translates machine outcome statuses into concise operational statements.
        """
        human_name = action_name.replace("_", " ").title()
        
        if outcome == "success":
            return f"The action '{human_name}' succeeded. Persistent storage confirmed."
        elif outcome == "failed":
            reason = details.get("reason", "Unknown internal transaction exception.")
            return f"The action '{human_name}' failed. Reason: {reason}"
        elif outcome == "blocked":
            reason = details.get("reason", "Security or write-guard policy constraint.")
            return f"The action '{human_name}' was blocked. Reason: {reason}"
        elif outcome == "needs_confirmation":
            return f"The action '{human_name}' requires explicit confirmation."
        elif outcome == "not_supported":
            return f"The action '{human_name}' is not supported in this environment."
        elif outcome == "queued":
            return f"The action '{human_name}' was queued for background execution."
        else:
            return f"The action '{human_name}' is in status: {outcome}."
