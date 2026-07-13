import logging
from typing import Dict, Any, List
from app.services.action_registry import ActionRegistry

logger = logging.getLogger("action_registry_inspector")

class ActionRegistryInspector:
    @classmethod
    def inspect_registry(cls) -> List[Dict[str, Any]]:
        """
        Inspects all action registry mappings, checking parameter signatures and schemas.
        """
        results = []
        for name, data in ActionRegistry.ACTIONS.items():
            schema = data.get("input_schema", {})
            issues = []
            if not schema:
                issues.append("Empty schema payload configuration.")
                
            results.append({
                "action_name": name,
                "has_schema": len(schema) > 0,
                "issues": issues,
                "requires_approval": data.get("requires_approval", False)
            })
            
            if issues:
                logger.warning(f"Action '{name}' validation issue detected: {', '.join(issues)}")
                
        return results
