import pytest
from app.services.specialist_delegation_policy import SpecialistDelegationPolicy

def test_specialist_delegation_policy_caps():
    SpecialistDelegationPolicy.reset_policy_limits()
    
    # Valid domain & type
    assert SpecialistDelegationPolicy.validate_delegation("CodeReviewerAgent", "code") is True
    
    # Invalid domain
    assert SpecialistDelegationPolicy.validate_delegation("CodeReviewerAgent", "unauthorized_domain") is False
    
    # Exceed recursion depth cap
    SpecialistDelegationPolicy.increment_counters(1.0)
    SpecialistDelegationPolicy.increment_counters(1.0)
    assert SpecialistDelegationPolicy.validate_delegation("CodeReviewerAgent", "code") is False
    
    # Reset
    SpecialistDelegationPolicy.reset_policy_limits()
    assert SpecialistDelegationPolicy.validate_delegation("CodeReviewerAgent", "code") is True
