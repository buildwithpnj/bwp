import logging
from typing import List, Dict, Any
from app.services.source_grounding_service import SourceGroundingService
from app.services.unsupported_claim_blocker import UnsupportedClaimBlocker
from app.services.final_answer_confidence_service import FinalAnswerConfidenceService

logger = logging.getLogger("final_grounding_guard")

class FinalGroundingGuard:
    @classmethod
    def validate_and_gate_response(
        cls,
        answer: str,
        evidence_chunks: List[Dict[str, Any]],
        base_confidence: float
    ) -> Dict[str, Any]:
        """
        Validates final answer grounding support, blocks unsupported claims, and sets final confidence.
        """
        # If no evidence chunks exist, block claims immediately
        if not evidence_chunks:
            logger.warning("Zero evidence chunks provided. Activating UnsupportedClaimBlocker.")
            return {
                "answer": UnsupportedClaimBlocker.block_fabricated_content(answer),
                "citations": [],
                "grounded": False,
                "confidence": 0.0
            }

        # Check grounding using standard overlap logic
        grounded_result = SourceGroundingService.ground_response(answer, evidence_chunks)
        
        # Calculate support score based on citations count vs chunks count
        support_score = FinalAnswerConfidenceService.calculate_support_score(
            answer,
            grounded_result.get("citations", []),
            base_confidence
        )

        final_answer = answer
        grounded = grounded_result.get("grounded", False)

        if support_score < 0.5:
            logger.error(f"Support score collapse detected (score: {support_score:.2f}). Blocking answer.")
            final_answer = UnsupportedClaimBlocker.block_fabricated_content(answer)
            grounded = False
        elif support_score < 0.8:
            logger.warning(f"Partial grounding detected (score: {support_score:.2f}). Downgrading certainty.")
            final_answer = f"Note: Some claims are partially supported. {answer}"

        return {
            "answer": final_answer,
            "citations": grounded_result.get("citations", []),
            "grounded": grounded,
            "confidence": support_score
        }
