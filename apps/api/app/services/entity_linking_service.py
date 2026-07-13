from typing import List

class EntityLinkingService:
    @classmethod
    def extract_entities(cls, query: str) -> List[str]:
        """
        Resolves query tokens into graph entities.
        """
        words = query.lower().split()
        return [w for w in words if len(w) > 4]
