from typing import List, Dict, Any
from app.services.action_registry import ActionRegistry

class ActionCapabilityService:
    @classmethod
    def get_capabilities(cls) -> List[Dict[str, Any]]:
        """
        Returns all registered action capabilities along with metadata.
        """
        capabilities = []
        for name, data in ActionRegistry.ACTIONS.items():
            capabilities.append({
                "action_name": name,
                "description": data["description"],
                "allowed_roles": data["allowed_roles"],
                "requires_approval": data["requires_approval"],
                "input_schema": {k: str(v) for k, v in data["input_schema"].items()}
            })
        return capabilities
