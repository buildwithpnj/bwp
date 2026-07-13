from typing import List, Dict, Any

class SourceGroundingService:
    @classmethod
    def ground_response(cls, answer: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates that response facts matches words present in reference chunks.
        """
        citations = []
        for chunk in chunks:
            summary_words = chunk["chunk_summary"].split()
            # check intersection match
            if any(w.lower() in answer.lower() for w in summary_words if len(w) > 3):
                citations.append({
                    "document_id": chunk["document_id"],
                    "chunk_id": chunk["chunk_id"],
                    "citation_text": chunk["chunk_summary"]
                })
        return {
            "answer": answer,
            "citations": citations,
            "grounded": len(citations) > 0
        }
