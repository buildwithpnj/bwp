import pytest
from app.services.preview_guardrails import PreviewGuardrails
from app.services.preview_budget_service import PreviewBudgetService

def test_guardrails_pass_initially():
    PreviewBudgetService.reset_daily_budget()
    session_id = "test_guardrails_sess"
    # Ensure stats are empty / reset
    stats = PreviewBudgetService.get_session_stats(session_id)
    stats["turns"] = 0
    stats["tokens"] = 0
    
    assert PreviewGuardrails.check_limits(session_id) is None

def test_guardrails_blocks_on_turn_limit():
    session_id = "test_guardrails_sess"
    stats = PreviewBudgetService.get_session_stats(session_id)
    stats["turns"] = PreviewGuardrails.MAX_TURNS
    
    reason = PreviewGuardrails.check_limits(session_id)
    assert reason is not None
    assert "turn limit" in reason.lower()
