from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class DelegationResponse(BaseModel):
    delegation_id: str
    specialist_type: str
    outcome_status: str  # succeeded, failed, timeout
    reasoning_summary: str
    structured_findings: Dict[str, Any] = Field(default_factory=dict)
    suggested_next_step: Dict[str, Any] = Field(default_factory=dict)
    suggested_recovery_path: Optional[str] = None
    confidence_score: float = 1.0
    used_tools: List[str] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
