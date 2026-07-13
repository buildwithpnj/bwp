from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime
from app.services.calendar_action_service import CalendarActionService

class CreateCalendarEventAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        start_time_str = payload["start_time"]
        end_time_str = payload["end_time"]
        
        # Parse ISO strings
        try:
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
        except Exception:
            start_time = datetime.now()
            end_time = datetime.now()
            
        event = await CalendarActionService.create_calendar_event(
            db, user_id, title, start_time, end_time
        )
        return {
            "status": "success",
            "event_id": event.id,
            "message": f"Calendar event '{title}' scheduled successfully."
        }
