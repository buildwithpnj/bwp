from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operating_thread import OperatingThread

class ThreadResumeService:
    @classmethod
    async def resume_thread(
        cls,
        db: AsyncSession,
        thread: OperatingThread
    ) -> OperatingThread:
        """
        Resumes a paused continuity thread workspace.
        """
        thread.status = "active"
        db.add(thread)
        await db.commit()
        return thread
