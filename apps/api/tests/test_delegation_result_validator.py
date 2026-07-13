import pytest
from app.services.delegation_result_validator import DelegationResultValidator
from app.schemas.delegation_response_schema import DelegationResponse

def test_delegation_result_validator_schema_bounds():
    resp_valid = DelegationResponse(
        delegation_id="del_1",
        specialist_type="CodeReviewerAgent",
        outcome_status="succeeded",
        reasoning_summary="Clean",
        confidence_score=0.9
    )
    assert DelegationResultValidator.validate(resp_valid) is True
    
    resp_invalid = DelegationResponse(
        delegation_id="del_2",
        specialist_type="",
        outcome_status="succeeded",
        reasoning_summary="No specialist name",
        confidence_score=-0.5
    )
    assert DelegationResultValidator.validate(resp_invalid) is False
