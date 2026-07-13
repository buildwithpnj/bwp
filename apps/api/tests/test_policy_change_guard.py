import pytest
from app.services.policy_change_guard import PolicyChangeGuard

def test_policy_shift_magnitude_gating():
    # Valid shift (0.2 difference)
    assert PolicyChangeGuard.validate_policy_shift(0.8, 0.6) is True
    
    # Invalid shift (0.6 difference)
    assert PolicyChangeGuard.validate_policy_shift(0.8, 0.2) is False
