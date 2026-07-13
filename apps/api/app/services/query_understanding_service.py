class QueryUnderstandingService:
    @classmethod
    def classify_intent(cls, query: str) -> str:
        """
        Classifies query intent profiles.
        """
        lower = query.lower()
        if "policy" in lower or "rule" in lower:
            return "governance_search"
        if "workflow" in lower or "action" in lower:
            return "workflow_search"
        return "broad_exploratory"
