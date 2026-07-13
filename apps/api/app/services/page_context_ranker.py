from typing import List, Dict, Any

class PageContextRanker:
    @classmethod
    def rank_context_items(cls, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritizes items based on urgency (e.g. failed steps rank above completed).
        """
        def score(item):
            status = item.get("status", "")
            if status == "failed":
                return 100
            elif status == "pending":
                return 50
            return 10
            
        return sorted(items, key=score, reverse=True)
