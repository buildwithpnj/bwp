from typing import Dict, Any
from app.services.source_grounding_service import SourceGroundingService

class RAGAnswerService:
    @classmethod
    def generate_answer(cls, query: str, compressed_pack: Dict[str, Any], confidence_score: float) -> Dict[str, Any]:
        """
        Builds a grounded, cited answer string based on context compression blocks.
        """
        if confidence_score < 0.6:
            return {
                "answer": "I cannot answer this question with sufficient confidence based on the current knowledge documents.",
                "citations": [],
                "grounded": False,
                "confidence_score": confidence_score
            }
            
        # simple mock generation
        doc_summaries = [b["summary"] for b in compressed_pack.get("evidence_blocks", [])]
        answer = f"Based on the knowledge base: {' and '.join(doc_summaries)}."
        
        grounded_data = SourceGroundingService.ground_response(answer, [
            {"document_id": "doc_1", "chunk_id": b["chunk_id"], "chunk_summary": b["summary"]}
            for b in compressed_pack.get("evidence_blocks", [])
        ])
        
        return {
            "answer": grounded_data["answer"],
            "citations": grounded_data["citations"],
            "grounded": grounded_data["grounded"],
            "confidence_score": confidence_score
        }
