import pytest
from app.services.preview_budget_service import PreviewBudgetService
from app.services.preview_guardrails import PreviewGuardrails

def test_daily_token_cap_reaches():
    PreviewBudgetService.reset_daily_budget()
    
    # Increment daily usage beyond cap
    PreviewBudgetService.increment_session("some_sess", PreviewGuardrails.MAX_TOKEN_BUDGET_DAILY + 100, 0.05)
    
    # Guardrails should block
    reason = PreviewGuardrails.check_limits("another_sess")
    assert reason is not None
    assert "daily budget" in reason.lower()
