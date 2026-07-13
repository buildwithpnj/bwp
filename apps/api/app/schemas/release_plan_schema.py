from pydantic import BaseModel, Field
from typing import List, Optional

class ReleasePlanCreate(BaseModel):
    rollout_id: str = Field(..., max_length=36)
    release_type: str = Field(..., max_length=50)  # e.g., policy_change, workflow_update
    target_scope: str = Field(..., max_length=100)
    canary_percentage: int = Field(10, ge=0, le=100)
    approval_required: bool = True
