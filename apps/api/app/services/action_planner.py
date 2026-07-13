from typing import Dict, Any, List
from app.schemas.action_plan import ActionPlan, ActionPlanStep
from app.services.tool_policy_service import ToolPolicyService

class ActionPlanner:
    @classmethod
    def propose_plan(cls, goal: str, user_id: str) -> ActionPlan:
        """
        Deduce execution steps based on a user's verbal or systemic goal.
        """
        steps = []
        reasoning = "To satisfy the user goal, compiling a sequence of action steps."
        
        goal_lower = goal.lower()
        if "weekly review" in goal_lower:
            steps.append(ActionPlanStep(
                action_name="generate_weekly_review",
                payload={"week_offset": 0}
            ))
            steps.append(ActionPlanStep(
                action_name="create_summary_note",
                payload={"topic": "Weekly Progress Summary", "notes": "Automated progress compilation completed."}
            ))
            reasoning = "Retrieving weekly performance metrics and saving them to the user notes archive."
            
        elif "coaching" in goal_lower or "escalate" in goal_lower:
            steps.append(ActionPlanStep(
                action_name="generate_contextual_coaching_prompt",
                payload={"weakness": "subject-verb agreement"}
            ))
            steps.append(ActionPlanStep(
                action_name="prepare_escalation_message_draft",
                payload={"reason": "low confidence threshold match"}
            ))
            reasoning = "Prepares target coaching advice and sets up an escalation email for manual review."
            
        else:
            # Default fallback step
            steps.append(ActionPlanStep(
                action_name="create_summary_note",
                payload={"topic": "General Summary", "notes": f"Coaching notes matching: {goal}"}
            ))
            reasoning = "Creating a summary note to capture the context request."

        # Compile risk score
        steps_dicts = [{"action_name": s.action_name, "payload": s.payload} for s in steps]
        risk = ToolPolicyService.calculate_plan_risk(steps_dicts)
        
        # Check if any step requires approval under default policy rules
        requires_approval = any(
            ToolPolicyService.requires_approval(s.action_name) for s in steps
        )
        
        return ActionPlan(
            goal=goal,
            reasoning_summary=reasoning,
            steps=steps,
            requires_approval=requires_approval,
            estimated_risk=risk,
            stop_conditions=["step_failure"],
            fallback_behavior="rollback"
        )
