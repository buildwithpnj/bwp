from typing import Dict, Any, Tuple
from app.services.action_registry import ActionRegistry

class ActionContractValidator:
    @classmethod
    def validate_action_contract(cls, action_name: str, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates payload structure dynamically using ActionRegistry.ACTIONS schema definitions.
        """
        if not isinstance(payload, dict):
            return False, "Payload must be a dictionary object."
            
        action = ActionRegistry.get_action(action_name)
        if not action:
            return False, f"Action '{action_name}' is not registered."
            
        schema = action["input_schema"]
        for key, expected_type in schema.items():
            if key not in payload:
                return False, f"Missing required parameter: '{key}'"
            if payload[key] is not None and not isinstance(payload[key], expected_type):
                return False, f"Parameter '{key}' must be of type {expected_type.__name__}."
                
        return True, "Contract check passed"

    @classmethod
    def validate_create_contract(cls, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Backwards compatibility helper for validating task creation payloads.
        """
        return cls.validate_action_contract("create_task", payload)
