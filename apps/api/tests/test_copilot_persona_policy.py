import pytest
from app.services.copilot_persona_policy import CopilotPersonaPolicy

def test_sanitize_reply_filler_removal():
    reply = "Sure! I can help you. Would you like to proceed? Great!"
    sanitized = CopilotPersonaPolicy.sanitize_reply(reply)
    # Check that filler is gone
    assert "Sure!" not in sanitized
    assert "Would you like to proceed?" not in sanitized
    assert "Great!" not in sanitized
    assert len(sanitized) > 0

def test_scrub_planning_artifacts():
    leaky_reply = "I will create a task. <action>{\"action_name\": \"create_task\", \"payload\": {}}</action> [action: create] check this."
    scrubbed = CopilotPersonaPolicy.scrub_planning_artifacts(leaky_reply)
    assert "<action>" not in scrubbed
    assert "create_task" not in scrubbed
    assert "[action: create]" not in scrubbed
    assert scrubbed == "I will create a task. check this."
