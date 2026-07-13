from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class CopilotContextPayload(BaseModel):
    current_route: str = Field(..., description="Active dashboard URL path route.")
    visible_module_hints: list = Field(default_factory=list)
    selected_entity_id: Optional[str] = None
    workflow_state: Optional[str] = None
