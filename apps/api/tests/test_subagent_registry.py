import pytest
from app.services.subagent_registry import SubAgentRegistry

def test_list_and_get_specialists():
    specialists = SubAgentRegistry.list_specialists()
    assert len(specialists) == 4
    assert "CodeReviewerAgent" in specialists
    assert "DatabaseAuditorAgent" in specialists
    
    cap = SubAgentRegistry.get_specialist("CodeReviewerAgent")
    assert cap is not None
    assert cap.purpose == "Audits Python models and services for security or compilation errors."
    assert "grep_search" in cap.allowed_tools
