from pydantic import BaseModel, Field
from typing import Optional

class OperatingThreadCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
