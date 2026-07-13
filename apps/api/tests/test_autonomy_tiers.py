import pytest
from app.services.tool_policy_service import ToolPolicyService

def test_autonomy_tier_0_always_requires_approval():
    # Even if action requires_approval is False, tier 0 requires approval
    assert ToolPolicyService.requires_approval("update_preference", autonomy_tier=0) is True
    assert ToolPolicyService.requires_approval("create_followup_practice", autonomy_tier=0) is True

def test_autonomy_tier_1_respects_action_defaults():
    # Respects defaults
    assert ToolPolicyService.requires_approval("update_preference", autonomy_tier=1) is False
    assert ToolPolicyService.requires_approval("create_followup_practice", autonomy_tier=1) is True
