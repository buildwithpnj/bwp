from typing import Dict, Any
from app.schemas.recovery_plan import RecoveryOption

class RecoveryPolicyService:
    @classmethod
    def evaluate_option(cls, action_type: str, description: str, parameters: Dict[str, Any]) -> RecoveryOption:
        """
        Assigns standard policy risk scores, approvals, and administrative gates
        for a given recovery action choice.
        """
        risk_score = 0.1
        requires_approval = True
        admin_only = False
        
        if action_type == "cancel_workflow":
            risk_score = 0.3
            requires_approval = True
            admin_only = False
        elif action_type == "switch_to_alternate":
            risk_score = 0.5
            requires_approval = True
            admin_only = False
        elif action_type == "escalate_to_admin":
            risk_score = 0.8
            requires_approval = True
            admin_only = True
            
        return RecoveryOption(
            action_type=action_type,
            description=description,
            risk_score=risk_score,
            requires_approval=requires_approval,
            admin_only=admin_only,
            parameters=parameters
        )
