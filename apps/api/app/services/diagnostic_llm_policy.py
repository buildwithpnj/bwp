import logging
from typing import List

logger = logging.getLogger("diagnostic_llm_policy")

class DiagnosticLlmPolicy:
    @classmethod
    def should_invoke_llm(cls, patterns: List[str], error_message: str) -> bool:
        """
        Determines if an LLM diagnostic summary should be generated.
        To avoid token waste, returns False if error is easily explained via heuristics.
        """
        err = error_message.lower()
        
        # 1. Simple heuristic validation errors don't need LLM
        if "validation" in err:
            logger.info("LLM Policy check: Skip LLM (simple Validation pattern).")
            return False
            
        # 2. Simple connection issues don't need LLM
        if "mock" in err or "connection" in err:
            logger.info("LLM Policy check: Skip LLM (simple Connection pattern).")
            return False
            
        # 3. If failure pattern is ambiguous, trigger LLM
        if not patterns:
            logger.info("LLM Policy check: Trigger LLM (Ambiguous failure).")
            return True
            
        return False
