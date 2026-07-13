import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.adaptive_delegation_policy_service import AdaptiveDelegationPolicyService

@pytest.mark.asyncio
async def test_adaptive_policy_tuning_based_on_feedback():
    db = AsyncMock()
    
    # Mock database to return average usefulness = 0.2, count = 3
    mock_res = MagicMock()
    mock_res.first.return_value = (0.2, 3)
    db.execute.return_value = mock_res
    
    # Should block since usefulness < 0.3
    allowed = await AdaptiveDelegationPolicyService.should_delegate_adaptive(
        db, "CodeReviewerAgent", "lesson_notes"
    )
    assert allowed is False
    
    # Mock database to return average usefulness = 0.8, count = 2
    mock_res_ok = MagicMock()
    mock_res_ok.first.return_value = (0.8, 2)
    db.execute.return_value = mock_res_ok
    
    # Should allow
    allowed_ok = await AdaptiveDelegationPolicyService.should_delegate_adaptive(
        db, "CodeReviewerAgent", "lesson_notes"
    )
    assert allowed_ok is True
    
    # Mock database to return count = 1 (not enough feedback history to block yet)
    mock_res_low_count = MagicMock()
    mock_res_low_count.first.return_value = (0.1, 1)
    db.execute.return_value = mock_res_low_count
    
    allowed_low_count = await AdaptiveDelegationPolicyService.should_delegate_adaptive(
        db, "CodeReviewerAgent", "lesson_notes"
    )
    assert allowed_low_count is True
