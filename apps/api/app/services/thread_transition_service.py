from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operating_thread import OperatingThread

class ThreadTransitionService:
    @classmethod
    async def transition_thread(
        cls,
        db: AsyncSession,
        thread: OperatingThread,
        new_status: str
    ) -> OperatingThread:
        """
        Transitions the user operating thread state to paused, archived, etc.
        """
        thread.status = new_status
        db.add(thread)
        await db.commit()
        return thread
