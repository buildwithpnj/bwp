from typing import List, Dict, Any
from app.services.planner_service import PlannerService
from app.services.step_budget_service import StepBudgetService
from app.services.loop_state_store import LoopStateStore
from app.services.loop_decision_service import LoopDecisionService
from app.services.tool_policy_guard import ToolPolicyGuard

class LoopOrchestrator:
    @classmethod
    def execute_loop(cls, task_prompt: str, tenant_id: str) -> Dict[str, Any]:
        """
        Coordinates plan decomposition and step iterations.
        """
        # Decompose task
        steps = PlannerService.plan_task(task_prompt)
        state_id = LoopStateStore.initialize_state(task_prompt, tenant_id)
        
        step_budget = StepBudgetService(max_steps=5)
        
        for step in steps:
            if not step_budget.has_budget():
                break
                
            # Enforce tool restrictions
            tool_name = step.get("tool")
            if tool_name and not ToolPolicyGuard.is_tool_allowed(tool_name, "read"):
                raise PermissionError(f"Tool '{tool_name}' is not authorized for read operations.")
                
            # Log step state
            LoopStateStore.append_step(state_id, step)
            step_budget.consume_step()
            
        final_decision = LoopDecisionService.evaluate_outcome(state_id)
        return {
            "state_id": state_id,
            "completed_steps": step_budget.steps_taken,
            "outcome": final_decision
        }
