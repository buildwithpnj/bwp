from pydantic import BaseModel, Field
from typing import Optional

class GovernanceUpdateRequest(BaseModel):
    tenant_id: str = Field(..., max_length=36)
    field_name: str = Field(..., max_length=100)
    new_value: str = Field(...)
