from pydantic import BaseModel, Field
from typing import Optional

class WorkflowControlRequest(BaseModel):
    control_type: str = Field(..., description="Action to perform: pause_workflow, resume_workflow, cancel_workflow, approve_checkpoint, reject_checkpoint, replay_failed_step, replay_workflow_from_step, force_recovery_review")
    reason: Optional[str] = Field(None, description="Optional justification for the control intervention.")
    step_index: Optional[int] = Field(None, description="Target step index for replay actions.")
