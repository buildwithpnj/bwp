from pydantic import BaseModel
from typing import Dict, Any, Optional

class RecoveryOption(BaseModel):
    action_type: str  # replay_failed_step, cancel_workflow, ask_user_context, switch_to_alternate
    description: str
    risk_score: float  # 0.0 to 1.0
    requires_approval: bool
    admin_only: bool
    parameters: Dict[str, Any] = {}
