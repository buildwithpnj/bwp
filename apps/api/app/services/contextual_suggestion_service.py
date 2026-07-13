from typing import List

class ContextualSuggestionService:
    @classmethod
    def generate_suggestions(cls, intent: str) -> List[str]:
        """
        Emits route-aware suggested actions context chips.
        """
        if intent == "stuck":
            return ["Explain last error", "Show recovery suggestions"]
        elif intent == "executing":
            return ["Show active tasks", "Pause workflow"]
        elif intent == "reviewing":
            return ["Verify current checkpoint", "Generate goals progress summary"]
        return ["Navigate to Diagnostics", "Check Active Tasks"]
