from typing import List, Dict, Any

class FinalAnswerConfidenceService:
    @classmethod
    def calculate_support_score(
        cls,
        answer: str,
        citations: List[Dict[str, Any]],
        base_confidence: float
    ) -> float:
        """
        Calculates grounding support score based on matching word overlaps.
        """
        if not citations:
            return 0.0
            
        answer_words = set(w.lower() for w in answer.split() if len(w) > 3)
        if not answer_words:
            return 0.0
            
        matching_words = set()
        for cit in citations:
            text = cit.get("citation_text", "")
            for word in text.split():
                w_low = word.lower()
                if len(w_low) > 3 and w_low in answer_words:
                    matching_words.add(w_low)
                    
        overlap_ratio = len(matching_words) / len(answer_words)
        
        # Weighted combination of base engine confidence and citation overlap ratio
        final_score = (base_confidence * 0.4) + (overlap_ratio * 0.6)
        return min(max(final_score, 0.0), 1.0)
