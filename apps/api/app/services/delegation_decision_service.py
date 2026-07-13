import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.services.specialist_delegation_policy import SpecialistDelegationPolicy

logger = logging.getLogger("delegation_decision_service")

class DelegationDecisionService:
    @classmethod
    async def evaluate_and_route(
        cls,
        db: AsyncSession,
        workflow_run_id: str,
        error_message: str,
        retry_count: int
    ) -> Optional[str]:
        """
        Determines the appropriate specialist subagent to route delegation based on failure context.
        """
        err = error_message.lower()
        
        target_specialist = None
        domain = None
        
        # 1. Routing Context Logic
        if "database" in err or "sqlite" in err or "foreign key" in err or "lock" in err:
            target_specialist = "DatabaseAuditorAgent"
            domain = "database"
        elif "syntax" in err or "attributeerror" in err or "import" in err:
            target_specialist = "CodeReviewerAgent"
            domain = "code"
        elif retry_count >= 2:
            target_specialist = "WorkflowDiagnosticianAgent"
            domain = "workflow_history"
            
        if not target_specialist:
            logger.info("Delegation Decision: No registered specialist pattern matches this context.")
            return None
            
        # 2. Verify with policy guard
        allowed = SpecialistDelegationPolicy.validate_delegation(target_specialist, domain)
        if not allowed:
            logger.info(f"Delegation Decision: Policy blocked trigger of {target_specialist}.")
            return None
            
        logger.info(f"Delegation Decision: Routing failed context to '{target_specialist}'.")
        return target_specialist
