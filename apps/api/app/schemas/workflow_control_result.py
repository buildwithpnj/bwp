from pydantic import BaseModel
from datetime import datetime

class WorkflowControlResult(BaseModel):
    workflow_run_id: str
    applied_at: datetime
    result_status: str  # applied, rejected, error
    message: str
