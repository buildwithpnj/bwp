from typing import Dict, Any

class PageAwareRetrievalService:
    @classmethod
    def inject_page_context(cls, page_scope: str, query: str) -> str:
        """
        Appends local page scope parameters to narrow broad searches.
        """
        if not page_scope:
            return query
        return f"[{page_scope}] {query}"
