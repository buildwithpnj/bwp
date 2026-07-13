from sqlalchemy.ext.asyncio import AsyncSession
from app.services.rollout_stage_manager import RolloutStageManager

class RollbackTriggerService:
    @classmethod
    async def evaluate_and_trigger(
        cls,
        db: AsyncSession,
        rollout_id: str,
        health_score: float
    ) -> bool:
        """
        Triggers auto-rollback if health score drops below threshold (0.5).
        """
        if health_score < 0.5:
            await RolloutStageManager.modify_rollout_status(db, rollout_id, "rollback")
            return True
        return False
