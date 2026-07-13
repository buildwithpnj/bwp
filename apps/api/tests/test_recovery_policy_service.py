import pytest
from app.services.recovery_policy_service import RecoveryPolicyService

def test_evaluate_recovery_option_gates():
    opt1 = RecoveryPolicyService.evaluate_option("replay_failed_step", "Replay", {})
    assert opt1.risk_score == 0.1
    assert opt1.requires_approval is True
    assert opt1.admin_only is False
    
    opt2 = RecoveryPolicyService.evaluate_option("escalate_to_admin", "Escalate", {})
    assert opt2.risk_score == 0.8
    assert opt2.requires_approval is True
    assert opt2.admin_only is True
