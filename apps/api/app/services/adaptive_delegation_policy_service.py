import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.delegation_policy_feedback import DelegationPolicyFeedback

logger = logging.getLogger("adaptive_delegation_policy_service")

class AdaptiveDelegationPolicyService:
    @classmethod
    async def should_delegate_adaptive(
        cls,
        db: AsyncSession,
        specialist_type: str,
        workflow_type: str
    ) -> bool:
        """
        Dynamically adjusts delegation gating by evaluating historical outcomes usefulness score averages.
        If past usefulness drops < 0.3, blocks future automatic specialist delegation queries.
        """
        stmt = select(
            func.avg(DelegationPolicyFeedback.usefulness_score),
            func.count(DelegationPolicyFeedback.id)
        ).where(
            DelegationPolicyFeedback.specialist_type == specialist_type,
            DelegationPolicyFeedback.workflow_type == workflow_type
        )
        
        res = await db.execute(stmt)
        avg_score, count = res.first() or (None, 0)
        
        if count >= 2 and avg_score is not None and avg_score < 0.3:
            logger.warning(f"Adaptive Gating: Blocking {specialist_type} on workflow {workflow_type} (Avg Usefulness={avg_score:.2f})")
            return False
            
        logger.info(f"Adaptive Gating: Allowed {specialist_type} (Count={count} Avg={avg_score})")
        return True
