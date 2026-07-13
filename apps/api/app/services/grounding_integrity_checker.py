from typing import List, Dict, Any

class GroundingIntegrityChecker:
    @classmethod
    def check_hallucination(cls, answer: str, citations: List[Dict[str, Any]]) -> bool:
        """
        Returns true if the answer contains details that do not align with cited snippets.
        """
        if not citations:
            return True
            
        # simple check: if key words are missing, flag as hallucination risk
        for cit in citations:
            text = cit.get("citation_text") or ""
            words = text.split()
            if any(w.lower() in answer.lower() for w in words if len(w) > 4):
                return False
        return True
