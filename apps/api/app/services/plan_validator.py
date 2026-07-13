from typing import Tuple, Optional, Set
from app.schemas.action_plan import ActionPlan
from app.services.action_registry import ActionRegistry
from app.services.tool_policy_service import ToolPolicyService

class PlanValidator:
    @classmethod
    def validate_plan(cls, plan: ActionPlan, user_role: str) -> Tuple[bool, Optional[str]]:
        """
        Validates an action plan for:
        - Registered actions & correct input validation schemas
        - Access authorization permissions
        - No circular step dependencies or duplicate loops
        """
        if not plan.steps:
            return False, "Plan has no execution steps."

        seen_steps = set()
        
        for idx, step in enumerate(plan.steps):
            action_name = step.action_name
            payload = step.payload
            
            # 1. Action existence
            action = ActionRegistry.get_action(action_name)
            if not action:
                return False, f"Step {idx}: Unknown action '{action_name}'."
                
            # 2. Input parameter schema validation
            if not ActionRegistry.validate_inputs(action_name, payload):
                return False, f"Step {idx}: Input payload schema validation failed for '{action_name}'."
                
            # 3. Access authorization check
            if not ToolPolicyService.is_allowed(action_name, user_role):
                return False, f"Step {idx}: Role '{user_role}' is not authorized to run action '{action_name}'."
                
            # 4. Cycle / Duplicate loop check
            step_signature = f"{action_name}:{sorted(payload.items())}"
            if step_signature in seen_steps:
                return False, f"Step {idx}: Circular execution loop detected on '{action_name}'."
            seen_steps.add(step_signature)
            
        return True, None
