from typing import Dict, Any, List
from app.services.action_registry import ActionRegistry

class ToolPolicyService:
    @classmethod
    def is_allowed(cls, action_name: str, user_role: str) -> bool:
        """Checks if a user role is authorized for the action."""
        action = ActionRegistry.get_action(action_name)
        if not action:
            return False
        return user_role in action["allowed_roles"]

    @classmethod
    def requires_approval(cls, action_name: str, autonomy_tier: int = 1) -> bool:
        """
        Gates approval requirement based on autonomy tier rules:
        - Tier 0: suggester only -> ALWAYS requires approval
        - Tier 1 & 2: auto-runs low-risk actions, requires approval for high-risk actions
        - Tier 3: requires approval only for risky state changes
        """
        action = ActionRegistry.get_action(action_name)
        if not action:
            return True
            
        if autonomy_tier == 0:
            return True
            
        # Default behavior: check action approval config
        return action["requires_approval"]

    @classmethod
    def calculate_plan_risk(cls, steps: List[Dict[str, Any]]) -> float:
        """
        Calculates cumulative risk score for a list of execution steps.
        Returns a score between 0.0 (no risk) and 1.0 (high risk/requires approval).
        """
        if not steps:
            return 0.0
            
        for step in steps:
            action_name = step.get("action_name")
            action = ActionRegistry.get_action(action_name)
            if not action:
                return 1.0  # Unknown action is high risk
            if action.get("requires_approval", False):
                return 1.0  # Any high-risk action makes the plan high risk
                
        return 0.2  # Low risk plan
