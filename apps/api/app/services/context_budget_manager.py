class ContextBudgetManager:
    @classmethod
    def check_context_overload(cls, current_tokens: int, limit: int = 4000) -> bool:
        """
        Detects if current context buffers exceed systemic token budget bounds.
        """
        return current_tokens > limit
