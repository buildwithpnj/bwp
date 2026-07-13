from pydantic import BaseModel, Field
from typing import Dict, Any

class NotificationAction(BaseModel):
    action_type: str = Field(..., description="Action category: e.g. approve, pause, resume, inspect, cancel")
    action_payload: Dict[str, Any] = Field(default_factory=dict)
