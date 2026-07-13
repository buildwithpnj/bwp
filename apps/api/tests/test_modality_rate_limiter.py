import pytest
from app.services.modality_rate_limiter import ModalityRateLimiter
from app.services.modality_governance_policy import ModalityGovernancePolicy

def test_rate_limiting_and_governance_limits():
    # 1. Rate limiter checks
    assert ModalityRateLimiter.check_rate_limit("tenant_abc", max_requests=2) is True
    assert ModalityRateLimiter.check_rate_limit("tenant_abc", max_requests=2) is True
    assert ModalityRateLimiter.check_rate_limit("tenant_abc", max_requests=2) is False
    
    # 2. File size ceiling checks
    assert ModalityGovernancePolicy.validate_file_size("pdf", 100000) is True
    assert ModalityGovernancePolicy.validate_file_size("pdf", 20000000) is False # > 15 MB limit
