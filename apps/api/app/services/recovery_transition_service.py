import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recovery_transition import RecoveryTransition

class RecoveryTransitionService:
    @classmethod
    async def log_recovery(
        cls,
        db: AsyncSession,
        scope: str
    ) -> RecoveryTransition:
        """
        Records details during system recovery steps.
        """
        trans = RecoveryTransition(
            id=str(uuid.uuid4()),
            affected_scope=scope,
            recovery_status="completed"
        )
        db.add(trans)
        await db.commit()
        return trans
