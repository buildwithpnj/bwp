import math
from typing import List, Dict, Any

class VectorStoreService:
    @classmethod
    def search_similar_vectors(
        cls,
        query_vector: List[float],
        candidates: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Calculates real cosine similarity values between vector listings.
        """
        scored = []
        for cand in candidates:
            cand_vector = cand.get("vector") or [0.1] * len(query_vector)
            
            # Real Cosine Similarity computation
            dot_product = sum(a * b for a, b in zip(query_vector, cand_vector))
            norm_a = math.sqrt(sum(a * a for a in query_vector))
            norm_b = math.sqrt(sum(b * b for b in cand_vector))
            
            score = 0.0
            if norm_a > 0.0 and norm_b > 0.0:
                score = dot_product / (norm_a * norm_b)
                
            scored.append({
                "chunk": cand,
                "score": score
            })
            
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
