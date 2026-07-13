from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.canary_rollout import CanaryRollout

class RolloutStageManager:
    @classmethod
    async def modify_rollout_status(
        cls,
        db: AsyncSession,
        rollout_id: str,
        action: str  # pause, resume, rollback
    ) -> CanaryRollout:
        """
        Manages stages transitions (pauses or resumes rollout execution).
        """
        stmt = select(CanaryRollout).where(CanaryRollout.rollout_id == rollout_id)
        res = await db.execute(stmt)
        canary = res.scalar_one_or_none()
        if not canary:
            raise ValueError("Rollout not found.")
            
        if action == "pause":
            canary.status = "paused"
        elif action == "resume":
            canary.status = "active"
        elif action == "rollback":
            canary.status = "rolled_back"
            
        db.add(canary)
        await db.commit()
        return canary
