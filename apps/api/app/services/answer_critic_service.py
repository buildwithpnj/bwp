from typing import List, Dict, Any

class AnswerCriticService:
    @classmethod
    def calculate_support_score(cls, answer: str, chunks: List[Dict[str, Any]]) -> float:
        """
        Computes support percentage.
        """
        if not chunks:
            return 0.0
            
        all_words = " ".join(c["chunk_text"].lower() for c in chunks)
        ans_words = [w for w in answer.lower().split() if len(w) > 4]
        
        if not ans_words:
            return 1.0
            
        matches = sum(1 for w in ans_words if w in all_words)
        return float(matches) / len(ans_words)
