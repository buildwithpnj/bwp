import pytest
from app.services.action_planner import ActionPlanner

def test_action_planner_weekly_review():
    plan = ActionPlanner.propose_plan("generate my weekly review summaries", "user_123")
    
    assert plan.goal == "generate my weekly review summaries"
    assert len(plan.steps) == 2
    assert plan.steps[0].action_name == "generate_weekly_review"
    assert plan.steps[1].action_name == "create_summary_note"
    assert plan.requires_approval is False  # both steps are auto-approved under default policy
    assert plan.estimated_risk == 0.2

def test_action_planner_coaching_escalation():
    plan = ActionPlanner.propose_plan("please escalate or provide coaching", "user_123")
    
    assert len(plan.steps) == 2
    assert plan.steps[0].action_name == "generate_contextual_coaching_prompt"
    assert plan.steps[1].action_name == "prepare_escalation_message_draft"
    assert plan.requires_approval is True  # prepare_escalation_message_draft requires approval
    assert plan.estimated_risk == 1.0
