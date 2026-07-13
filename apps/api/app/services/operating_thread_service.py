import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operating_thread import OperatingThread
from app.schemas.operating_thread_schema import OperatingThreadCreate

class OperatingThreadService:
    @classmethod
    async def create_thread(
        cls,
        db: AsyncSession,
        user_id: str,
        data: OperatingThreadCreate
    ) -> OperatingThread:
        """
        Creates a new user operating thread to preserve cross-page continuity.
        """
        thread = OperatingThread(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=data.title,
            description=data.description,
            status="active"
        )
        db.add(thread)
        await db.commit()
        return thread
