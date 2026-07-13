import logging
from typing import Dict, Any, List
from app.services.llm_provider_router import LLMProviderRouter
from app.services.source_grounding_service import SourceGroundingService

logger = logging.getLogger("local_grounded_answer")

class LocalGroundedAnswerService:
    @classmethod
    async def generate_grounded_answer(
        cls,
        query: str,
        compressed_pack: Dict[str, Any],
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Builds a grounded, cited answer string based on context compression blocks using the local model.
        """
        if confidence_score < 0.6:
            return {
                "answer": "I cannot answer this question with sufficient confidence based on the current knowledge documents.",
                "citations": [],
                "grounded": False,
                "confidence_score": confidence_score
            }

        evidence_blocks = compressed_pack.get("evidence_blocks", [])
        if not evidence_blocks:
            return {
                "answer": "No relevant context files found in local database. I must abstain from answering.",
                "citations": [],
                "grounded": False,
                "confidence_score": 0.0
            }

        # Build prompt instructing the model on citations
        context_str = "\n".join([
            f"Document ID: doc_1 | Chunk ID: {b.get('chunk_id')} | Summary: {b.get('summary')}"
            for b in evidence_blocks
        ])

        system_instruction = (
            "You are a production RAG inference assistant. Answer the user query using only the provided context block. "
            "Cite the context blocks in your response by using their summary text matches."
        )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuery: {query}"}
        ]

        logger.info(f"Generating local grounded response for query: '{query}'...")
        result = await LLMProviderRouter.route_completion(
            messages=messages,
            json_mode=False
        )

        if result.get("status") != "success":
            return {
                "answer": "Local LLM service failed to generate response. Fallback to default safety warning.",
                "citations": [],
                "grounded": False,
                "confidence_score": confidence_score
            }

        answer_content = result.get("content", "")

        # Ground response using SourceGroundingService
        chunks_for_grounding = [
            {
                "document_id": "doc_1",
                "chunk_id": b.get("chunk_id"),
                "chunk_summary": b.get("summary")
            }
            for b in evidence_blocks
        ]

        grounded_data = SourceGroundingService.ground_response(answer_content, chunks_for_grounding)

        # Handle low grounding / zero citations fallback
        if not grounded_data["grounded"]:
            logger.warning("Local inference model produced zero citations from RAG context. Abasing response.")
            return {
                "answer": "I cannot ground my answer within the provided context. Abstaining from answering.",
                "citations": [],
                "grounded": False,
                "confidence_score": confidence_score
            }

        return {
            "answer": grounded_data["answer"],
            "citations": grounded_data["citations"],
            "grounded": grounded_data["grounded"],
            "confidence_score": confidence_score
        }
