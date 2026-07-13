import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.canary_rollout import CanaryRollout

class CanaryRolloutService:
    @classmethod
    async def initiate_rollout(
        cls,
        db: AsyncSession,
        rollout_id: str,
        initial_percentage: int = 10
    ) -> CanaryRollout:
        """
        Launches canary stages with default percentage gates.
        """
        canary = CanaryRollout(
            rollout_id=rollout_id,
            canary_percentage=initial_percentage,
            status="active"
        )
        db.add(canary)
        await db.commit()
        return canary
        
    @classmethod
    async def update_percentage(
        cls,
        db: AsyncSession,
        rollout_id: str,
        new_percentage: int
    ) -> CanaryRollout:
        """
        Expands canary rollout range.
        """
        stmt = select(CanaryRollout).where(CanaryRollout.rollout_id == rollout_id)
        res = await db.execute(stmt)
        canary = res.scalar_one_or_none()
        if not canary:
            raise ValueError("Rollout not found.")
            
        canary.canary_percentage = new_percentage
        db.add(canary)
        await db.commit()
        return canary
