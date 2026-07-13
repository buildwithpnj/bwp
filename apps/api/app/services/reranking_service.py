from typing import List, Dict, Any

class RerankingService:
    @classmethod
    def reorder_candidates(cls, query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Reranks chunk candidates based on query term matches count.
        """
        scored = []
        for cand in candidates:
            # count word intersections
            query_words = set(query.lower().split())
            text_words = set(cand["chunk_text"].lower().split())
            intersection = query_words.intersection(text_words)
            
            score = 0.5 + 0.1 * len(intersection)
            scored.append({
                "chunk_id": cand["chunk_id"],
                "document_id": cand["document_id"],
                "chunk_text": cand["chunk_text"],
                "chunk_summary": cand["chunk_summary"],
                "confidence_score": min(score, 1.0)
            })
            
        scored.sort(key=lambda x: x["confidence_score"], reverse=True)
        return scored
