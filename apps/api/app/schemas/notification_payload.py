from pydantic import BaseModel, Field
from typing import Optional

class NotificationPayload(BaseModel):
    source_type: str = Field(..., description="Alert category: e.g. workflow_failure, quota_exceeded")
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    priority: str = "medium"
