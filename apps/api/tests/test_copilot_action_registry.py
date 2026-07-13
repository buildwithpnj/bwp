import pytest
from app.services.copilot_action_registry import CopilotActionRegistry
from app.services.action_policy_registry import ActionPolicyTier

def test_copilot_action_registry_listing():
    actions = CopilotActionRegistry.list_actions()
    # Should have 49 actions
    assert len(actions) == 49
    assert "create_note" in actions
    assert "create_task" in actions
    assert "permanent_purge_item" in actions

def test_copilot_action_details():
    action = CopilotActionRegistry.get_action("create_note")
    assert action is not None
    assert action["module"] == "notes"
    assert action["policy_tier"] == ActionPolicyTier.SAFE_AUTO
    assert action["requires_approval"] is False

    purge_action = CopilotActionRegistry.get_action("permanent_purge_item")
    assert purge_action is not None
    assert purge_action["module"] == "trash"
    assert purge_action["policy_tier"] == ActionPolicyTier.ADMIN_ONLY
    assert purge_action["requires_approval"] is False
