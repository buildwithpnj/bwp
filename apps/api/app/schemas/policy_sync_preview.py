from pydantic import BaseModel
from app.schemas.policy_diff_schema import PolicyDiffSchema

class PolicySyncPreview(BaseModel):
    diff: PolicyDiffSchema
    has_drift: bool
    requires_approval: bool
