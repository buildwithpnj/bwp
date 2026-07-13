import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.degraded_mode_activation import DegradedModeActivation

class DegradedModeManager:
    @classmethod
    async def activate_degraded(
        cls,
        db: AsyncSession,
        scope: str,
        active_features: str,
        disabled_features: str
    ) -> DegradedModeActivation:
        """
        Activates degradation level bounds (e.g. switches model calls to Ollama fallbacks).
        """
        act = DegradedModeActivation(
            id=str(uuid.uuid4()),
            affected_scope=scope,
            activated_features=active_features,
            disabled_features=disabled_features
        )
        db.add(act)
        await db.commit()
        return act
