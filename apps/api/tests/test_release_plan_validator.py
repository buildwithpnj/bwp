import pytest
from app.services.release_plan_validator import ReleasePlanValidator
from app.services.release_safety_score_service import ReleaseSafetyScoreService

def test_release_plan_validation():
    # 1. Scope and percentage boundaries
    assert ReleasePlanValidator.validate_plan_readiness("staging", 50) is True
    assert ReleasePlanValidator.validate_plan_readiness("staging", 150) is False
    assert ReleasePlanValidator.validate_plan_readiness("", 20) is False
    
    # 2. Risk scoring calculation
    assert ReleaseSafetyScoreService.calculate_safety_score(True, 0.0) == 0.7  # Drift penalty
    assert ReleaseSafetyScoreService.calculate_safety_score(False, 0.2) == 0.6  # Failure spike penalty
