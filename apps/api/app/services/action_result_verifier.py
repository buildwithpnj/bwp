import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.goals import Goal
from app.models.notes import Note
from app.models.calendar_event import CalendarEvent
from app.models.user_profile_memory import UserProfileMemory

logger = logging.getLogger("action_result_verifier")

class ActionResultVerifier:
    @classmethod
    async def verify_task_created(cls, db: AsyncSession, task_id: str) -> bool:
        db.expire_all()
        stmt = select(Goal).where(Goal.id == task_id)
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        is_verified = record is not None
        if is_verified:
            logger.info(f"Factual Verification Success: Task {task_id} exists in persistent storage.")
        else:
            logger.error(f"Factual Verification Failure: Task {task_id} missing from database tables.")
        return is_verified

    @classmethod
    async def verify_task_status(cls, db: AsyncSession, task_id: str, expected_status: str) -> bool:
        db.expire_all()
        stmt = select(Goal).where(Goal.id == task_id)
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            return False
        is_matching = record.status == expected_status
        if is_matching:
            logger.info(f"Factual Verification Success: Task {task_id} status matches '{expected_status}'.")
        else:
            logger.error(f"Factual Verification Failure: Task {task_id} status is '{record.status}', expected '{expected_status}'.")
        return is_matching

    @classmethod
    async def verify_note_created(cls, db: AsyncSession, note_id: str) -> bool:
        db.expire_all()
        stmt = select(Note).where(Note.id == note_id)
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        return record is not None

    @classmethod
    async def verify_calendar_event_created(cls, db: AsyncSession, event_id: str) -> bool:
        db.expire_all()
        stmt = select(CalendarEvent).where(CalendarEvent.id == event_id)
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        return record is not None

    @classmethod
    async def verify_memory_item_created(cls, db: AsyncSession, memory_id: str) -> bool:
        db.expire_all()
        stmt = select(UserProfileMemory).where(UserProfileMemory.id == memory_id)
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        return record is not None

    @classmethod
    async def verify_project_item_created(cls, db: AsyncSession, project_item_id: str) -> bool:
        db.expire_all()
        # Defer import to prevent circular dependencies before migration runs
        try:
            from app.models.project_item import ProjectItem
            stmt = select(ProjectItem).where(ProjectItem.id == project_item_id)
            result = await db.execute(stmt)
            record = result.scalar_one_or_none()
            return record is not None
        except Exception as e:
            logger.error(f"Project item model import or query failed: {e}")
            return False
            
    @classmethod
    async def verify_project_item_updated(cls, db: AsyncSession, project_item_id: str, expected_status: str) -> bool:
        db.expire_all()
        try:
            from app.models.project_item import ProjectItem
            stmt = select(ProjectItem).where(ProjectItem.id == project_item_id)
            result = await db.execute(stmt)
            record = result.scalar_one_or_none()
            if not record:
                return False
            return record.status == expected_status
        except Exception as e:
            logger.error(f"Project item status verification failed: {e}")
            return False
