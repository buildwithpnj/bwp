import pytest
from app.services.action_response_formatter import ActionResponseFormatter
from app.services.copilot_response_style_service import CopilotResponseStyleService
from app.services.user_facing_outcome_renderer import UserFacingOutcomeRenderer

def test_response_formatting_structure():
    res = ActionResponseFormatter.format_response(
        status="success",
        action_name="create_note",
        result="Successfully created note",
        scope="workspace",
        next_steps="Verify note in list"
    )
    assert "Status: Success" in res
    assert "Action: Create Note" in res
    assert "Scope: workspace" in res
    assert "Next: Verify note in list" in res

def test_response_style_sanitization():
    raw_response = "Sure thing! I created the note. Done :) Anything else?"
    sanitized = CopilotResponseStyleService.sanitize_response(raw_response)
    assert "Sure thing!" not in sanitized
    assert "Done :)" not in sanitized
    assert "Anything else?" not in sanitized

def test_user_facing_outcome_rendering():
    outcome_msg = UserFacingOutcomeRenderer.render_outcome(
        outcome="blocked",
        action_name="delete_all_files",
        details={"reason": "requires admin rights"}
    )
    assert "was blocked" in outcome_msg
    assert "requires admin rights" in outcome_msg
