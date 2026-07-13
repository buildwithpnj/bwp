import pytest
from app.schemas.action_plan import ActionPlan, ActionPlanStep
from app.services.plan_validator import PlanValidator

def test_plan_validator_success():
    # Valid plan
    steps = [
        ActionPlanStep(action_name="generate_weekly_review", payload={"week_offset": 0}),
        ActionPlanStep(action_name="create_summary_note", payload={"topic": "Review", "notes": "Compiling results"})
    ]
    plan = ActionPlan(goal="review", reasoning_summary="test reasoning", steps=steps)
    
    is_valid, err = PlanValidator.validate_plan(plan, "approved_user")
    assert is_valid is True
    assert err is None

def test_plan_validator_unknown_action():
    # Plan has unknown action name
    steps = [
        ActionPlanStep(action_name="unknown_action_name", payload={})
    ]
    plan = ActionPlan(goal="unknown", reasoning_summary="test reasoning", steps=steps)
    
    is_valid, err = PlanValidator.validate_plan(plan, "approved_user")
    assert is_valid is False
    assert "Unknown action" in err

def test_plan_validator_circular_loop():
    # Plan has circular duplicate step loop
    steps = [
        ActionPlanStep(action_name="create_summary_note", payload={"topic": "A", "notes": "B"}),
        ActionPlanStep(action_name="create_summary_note", payload={"topic": "A", "notes": "B"})
    ]
    plan = ActionPlan(goal="loop", reasoning_summary="test reasoning", steps=steps)
    
    is_valid, err = PlanValidator.validate_plan(plan, "approved_user")
    assert is_valid is False
    assert "Circular execution loop" in err
