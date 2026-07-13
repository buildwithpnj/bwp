from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class RealTimeEvent(BaseModel):
    event_id: str
    event_type: str  # action.suggested, workflow.started, etc.
    occurred_at: datetime
    tenant_id: Optional[str] = None
    user_id: str
    workflow_run_id: Optional[str] = None
    action_log_id: Optional[str] = None
    step_id: Optional[str] = None
    execution_status: Optional[str] = None
    recovery_status: Optional[str] = None
    summary_message: Optional[str] = None
    safe_metadata: Dict[str, Any] = Field(default_factory=dict)
