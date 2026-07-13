from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class DelegationRequest(BaseModel):
    delegation_id: str
    workflow_run_id: str
    action_log_id: Optional[str] = None
    parent_step_id: Optional[str] = None
    requesting_agent: str
    specialist_type: str
    delegation_reason: str
    bounded_goal: str
    provided_context: Dict[str, Any] = Field(default_factory=dict)
    allowed_tools: List[str] = Field(default_factory=list)
    max_steps: int = 5
    timeout_ms: int = 5000
    created_at: datetime = Field(default_factory=datetime.utcnow)
