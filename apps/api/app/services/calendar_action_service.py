import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.calendar_event import CalendarEvent
from typing import Dict, Any, Optional

logger = logging.getLogger("calendar_action_service")

class CalendarActionService:
    @classmethod
    async def create_calendar_event(
        cls,
        db: AsyncSession,
        user_id: str,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None
    ) -> CalendarEvent:
        """
        Creates a new calendar event entry.
        """
        event = CalendarEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            timezone="UTC"
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        logger.info(f"Created calendar event: {event.id} for user: {user_id}")
        return event
