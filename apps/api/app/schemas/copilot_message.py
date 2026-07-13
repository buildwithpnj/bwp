from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class CopilotMessage(BaseModel):
    role: str = Field(..., description="Role: user or assistant.")
    content: str = Field(..., description="Message text or transcription.")
    suggested_action: Optional[Dict[str, Any]] = None
