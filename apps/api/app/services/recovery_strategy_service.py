from typing import List

class RecoveryStrategyService:
    @classmethod
    def suggest_recovery_query(cls, original_query: str, missing_keywords: List[str]) -> str:
        """
        Builds a modified query targeting semantic gaps.
        """
        if not missing_keywords:
            return original_query
        return f"{original_query} {' '.join(missing_keywords)}"
