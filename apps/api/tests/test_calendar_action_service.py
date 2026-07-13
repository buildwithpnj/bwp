import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from app.services.calendar_action_service import CalendarActionService

@pytest.mark.asyncio
async def test_create_calendar_event_success():
    db = AsyncMock()
    start_time = datetime.now(timezone.utc)
    end_time = datetime.now(timezone.utc)
    
    event = await CalendarActionService.create_calendar_event(
        db=db,
        user_id="user_888",
        title="Check release gates",
        start_time=start_time,
        end_time=end_time,
        description="Verify V0.50 automated release tasks"
    )
    
    assert event.user_id == "user_888"
    assert event.title == "Check release gates"
    assert event.timezone == "UTC"
    assert db.add.called
    assert db.commit.called
