from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class ActionApprovalRequestCreate(BaseModel):
    action_name: str
    action_payload: Dict[str, Any]
    tenant_id: Optional[str] = None
    session_id: Optional[str] = None

class ActionApprovalRequestResponse(BaseModel):
    id: str
    tenant_id: Optional[str]
    user_id: str
    session_id: Optional[str]
    action_name: str
    module_name: Optional[str]
    policy_tier: str
    risk_level: str
    target_type: Optional[str]
    target_id: Optional[str]
    action_payload: Dict[str, Any]
    human_summary: Optional[str]
    execution_preview: Optional[str]
    created_at: datetime
    expires_at: datetime
    status: str
    approved_by: Optional[str]
    denied_by: Optional[str]
    audit_id: Optional[str]

    class Config:
        from_attributes = True

class ApprovalDecisionInput(BaseModel):
    approve: bool
    token: Optional[str] = None
