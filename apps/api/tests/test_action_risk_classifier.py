import pytest
from app.services.action_risk_classifier import ActionRiskClassifier
from app.services.action_policy_registry import ActionPolicyTier

def test_risk_classification():
    # Safe auto-run actions
    assert ActionRiskClassifier.classify_action("create_note", {"title": "Hello"}) == ActionPolicyTier.SAFE_AUTO
    
    # Destructive actions
    assert ActionRiskClassifier.classify_action("delete_note", {"note_id": "123"}) == ActionPolicyTier.DESTRUCTIVE_CONFIRMED

def test_settings_preference_escalation():
    # Regular preference - CONFIRM_FIRST
    tier = ActionRiskClassifier.classify_action(
        "update_settings_preference", 
        {"key": "timezone", "value": "America/New_York"}
    )
    assert tier == ActionPolicyTier.CONFIRM_FIRST

    # Sensitive preference - ADMIN_ONLY escalation
    for sensitive_key in ["admin_password", "jwt_secret", "encryption_key", "api_key"]:
        tier = ActionRiskClassifier.classify_action(
            "update_settings_preference", 
            {"key": sensitive_key, "value": "super-secret-value"}
        )
        assert tier == ActionPolicyTier.ADMIN_ONLY
