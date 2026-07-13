class ZeroHitFallbackService:
    @classmethod
    def get_fallback_suggestions(cls, query: str) -> list:
        """
        Suggests spelling fixes or synonym options for queries returning zero matching documents.
        """
        lower = query.lower()
        if "polic" in lower:
            return ["policy sync", "system governance configuration"]
        return ["internal wiki guides", "workflow automation controls"]
