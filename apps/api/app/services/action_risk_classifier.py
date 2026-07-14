from typing import Dict, Any
from app.services.action_policy_registry import ActionPolicyRegistry, ActionPolicyTier

class ActionRiskClassifier:
    @classmethod
    def classify_action(cls, action_name: str, payload: Dict[str, Any]) -> ActionPolicyTier:
        """
        Dynamically classifies the risk tier of an action based on its name and payload.
        Allows for runtime escalation of risk levels based on input values.
        """
        tier = ActionPolicyRegistry.get_policy(action_name)
        
        # Dynamic risk escalation logic
        if action_name == "update_settings_preference":
            key = payload.get("key", "")
            # Escalates to ADMIN_ONLY if sensitive parameters are updated
            if key in ["admin_password", "jwt_secret", "encryption_key", "api_key"]:
                return ActionPolicyTier.ADMIN_ONLY

        if action_name == "purge_trash":
            # If purging trash without confirmation, escalate to DESTRUCTIVE_CONFIRMED (already is)
            return ActionPolicyTier.DESTRUCTIVE_CONFIRMED

        return tier
