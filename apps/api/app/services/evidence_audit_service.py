from typing import List, Dict, Any

class EvidenceAuditService:
    @classmethod
    def audit_evidence(cls, chunks: List[Dict[str, Any]]) -> str:
        """
        Assesses confidence based on matched relevance count of reference chunks.
        """
        if not chunks:
            return "insufficient"
            
        avg_score = sum(c.get("score") or 0.5 for c in chunks) / len(chunks)
        if avg_score > 0.8:
            return "strong"
        elif avg_score > 0.5:
            return "moderate"
        return "weak"
