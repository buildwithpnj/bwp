import pytest
from app.services.action_policy_registry import ActionPolicyRegistry, ActionPolicyTier

def test_action_policy_mappings():
    # SAFE_AUTO
    assert ActionPolicyRegistry.get_policy("create_note") == ActionPolicyTier.SAFE_AUTO
    assert ActionPolicyRegistry.get_policy("create_task") == ActionPolicyTier.SAFE_AUTO
    assert ActionPolicyRegistry.get_policy("search_knowledge") == ActionPolicyTier.SAFE_AUTO
    assert ActionPolicyRegistry.get_policy("get_recent_updates") == ActionPolicyTier.SAFE_AUTO
    assert ActionPolicyRegistry.get_policy("get_agent_status") == ActionPolicyTier.SAFE_AUTO

    # CONFIRM_FIRST
    assert ActionPolicyRegistry.get_policy("update_task") == ActionPolicyTier.CONFIRM_FIRST
    assert ActionPolicyRegistry.get_policy("archive_note") == ActionPolicyTier.CONFIRM_FIRST
    assert ActionPolicyRegistry.get_policy("move_task_to_project") == ActionPolicyTier.CONFIRM_FIRST
    assert ActionPolicyRegistry.get_policy("update_calendar_event") == ActionPolicyTier.CONFIRM_FIRST
    assert ActionPolicyRegistry.get_policy("update_settings_preference") == ActionPolicyTier.CONFIRM_FIRST

    # DESTRUCTIVE_CONFIRMED
    assert ActionPolicyRegistry.get_policy("delete_note") == ActionPolicyTier.DESTRUCTIVE_CONFIRMED
    assert ActionPolicyRegistry.get_policy("delete_task") == ActionPolicyTier.DESTRUCTIVE_CONFIRMED
    assert ActionPolicyRegistry.get_policy("delete_project") == ActionPolicyTier.DESTRUCTIVE_CONFIRMED
    assert ActionPolicyRegistry.get_policy("permanently_delete_item") == ActionPolicyTier.DESTRUCTIVE_CONFIRMED
    assert ActionPolicyRegistry.get_policy("purge_trash") == ActionPolicyTier.DESTRUCTIVE_CONFIRMED

    # ADMIN_ONLY
    assert ActionPolicyRegistry.get_policy("reveal_sensitive_config") == ActionPolicyTier.ADMIN_ONLY
    assert ActionPolicyRegistry.get_policy("delete_shared_workspace_resources") == ActionPolicyTier.ADMIN_ONLY
    assert ActionPolicyRegistry.get_policy("modify_system_policies") == ActionPolicyTier.ADMIN_ONLY
    assert ActionPolicyRegistry.get_policy("access_restricted_credentials") == ActionPolicyTier.ADMIN_ONLY
