import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.resilience_state import ResilienceState
from app.schemas.resilience_policy_schema import ResiliencePolicyCreate

class ResiliencePolicyService:
    @classmethod
    async def configure_policy(
        cls,
        db: AsyncSession,
        req: ResiliencePolicyCreate
    ) -> ResilienceState:
        """
        Saves resilience state thresholds.
        """
        policy = ResilienceState(
            id=str(uuid.uuid4()),
            trigger_type=req.trigger_type,
            affected_scope=req.affected_scope,
            degradation_level=req.degradation_level,
            token_budget_reduction_factor=req.token_budget_reduction_factor
        )
        db.add(policy)
        await db.commit()
        return policy
