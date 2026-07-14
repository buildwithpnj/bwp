from typing import List, Dict, Any
from app.services.copilot_action_registry import CopilotActionRegistry

class ActionCapabilityService:
    @classmethod
    def get_capabilities(cls) -> List[Dict[str, Any]]:
        """
        Returns all registered action capabilities along with metadata, modules, and policy tiers.
        """
        capabilities = []
        for name in CopilotActionRegistry.list_actions():
            data = CopilotActionRegistry.get_action(name)
            if data:
                # Convert the input schema to string representation for JSON compatibility
                schema_dict = {}
                if data.get("pydantic_schema"):
                    try:
                        # If schema is a Pydantic model
                        schema_dict = {k: str(v.annotation) for k, v in data["pydantic_schema"].model_fields.items()}
                    except AttributeError:
                        schema_dict = {k: str(v) for k, v in data["pydantic_schema"].items()}

                capabilities.append({
                    "action_name": name,
                    "description": data.get("description", ""),
                    "allowed_roles": data.get("allowed_roles", []),
                    "requires_approval": data.get("requires_approval", False),
                    "policy_tier": data.get("policy_tier", "confirm_first"),
                    "module": data.get("module", "general"),
                    "input_schema": schema_dict
                })
        return capabilities
