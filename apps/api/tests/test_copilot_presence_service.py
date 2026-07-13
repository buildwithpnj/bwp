import pytest
from app.services.copilot_presence_service import CopilotPresenceService
from app.services.contextual_suggestion_service import ContextualSuggestionService

def test_copilot_presence_heuristics():
    # 1. stuck intent
    res = CopilotPresenceService.evaluate_presence("/diagnostics")
    assert res["intent"] == "stuck"
    assert res["directive"] == "suggest_recovery"
    
    # 2. active work execution intent
    res_exec = CopilotPresenceService.evaluate_presence("/workspace")
    assert res_exec["intent"] == "executing"
    assert res_exec["directive"] == "stay_silent"
    
    # 3. contextual suggestions
    chips = ContextualSuggestionService.generate_suggestions("stuck")
    assert "Explain last error" in chips
