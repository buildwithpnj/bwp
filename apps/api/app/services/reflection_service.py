from typing import List, Dict, Any
from app.services.evidence_gap_detector import EvidenceGapDetector
from app.services.answer_critic_service import AnswerCriticService
from app.services.recovery_strategy_service import RecoveryStrategyService

class ReflectionService:
    @classmethod
    def critique_generation(
        cls,
        query: str,
        answer: str,
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Performs self-critique audits on output grounding.
        """
        gaps = EvidenceGapDetector.find_gaps(query, chunks)
        score = AnswerCriticService.calculate_support_score(answer, chunks)
        
        should_retry = score < 0.6 or len(gaps) > 0
        recovery = None
        if should_retry:
            recovery = RecoveryStrategyService.suggest_recovery_query(query, gaps)
            
        return {
            "support_score": score,
            "evidence_gaps": gaps,
            "should_retry": should_retry,
            "recovery_strategy": recovery
        }
