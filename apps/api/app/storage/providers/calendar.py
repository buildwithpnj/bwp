from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class CalendarProvider(ABC):
    """Abstract Base Class defining the interface for Calendar Providers in Warborn OS.
    
    Provides placeholders to prepare the architecture for Google Calendar and other calendar services
    without requesting permission or implementing logic yet.
    """

    @abstractmethod
    async def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        **kwargs: Any
    ) -> str:
        """Create a new event in the calendar. Returns the event ID."""
        pass

    @abstractmethod
    async def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """Update an existing event details in the calendar."""
        pass

    @abstractmethod
    async def delete_event(self, event_id: str, **kwargs: Any) -> None:
        """Delete an event from the calendar."""
        pass

    @abstractmethod
    async def list_events(
        self,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 100,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """List upcoming events in the calendar within a specified time range."""
        pass

    @abstractmethod
    async def check_availability(
        self,
        start_time: datetime,
        end_time: datetime,
        **kwargs: Any
    ) -> bool:
        """Check if the calendar is free/available during the specified slot."""
        pass
