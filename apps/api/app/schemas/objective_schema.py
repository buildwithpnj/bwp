from pydantic import BaseModel, Field
from typing import Optional

class ObjectiveCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    stop_condition: Optional[str] = None
