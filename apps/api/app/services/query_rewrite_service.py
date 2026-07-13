class QueryRewriteService:
    @classmethod
    def expand_query(cls, query: str) -> str:
        """
        Expands abbreviations or keywords in query string for higher match rates.
        """
        lower = query.lower()
        if "sync" in lower:
            return query + " policy synchronization cluster drift"
        return query
