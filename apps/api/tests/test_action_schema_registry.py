import pytest
from app.services.copilot_action_registry import CopilotActionRegistry

def test_note_schema_validation():
    # Valid
    payload = {"title": "Daily Standup", "content": "Met with team.", "tags": "work,standup"}
    assert CopilotActionRegistry.validate_inputs("create_note", payload)

    # Invalid title empty
    bad_payload = {"title": "", "content": "Met with team."}
    assert not CopilotActionRegistry.validate_inputs("create_note", bad_payload)

def test_task_schema_validation():
    # Valid
    payload = {"title": "Fix alignment", "description": "Fix alignment of Next.js dev server dashboard button", "category": "bug"}
    assert CopilotActionRegistry.validate_inputs("create_task", payload)

    # Invalid title too long (over 255 chars)
    bad_payload = {"title": "A" * 260}
    assert not CopilotActionRegistry.validate_inputs("create_task", bad_payload)

def test_calendar_schema_validation():
    payload = {"title": "Sync meeting", "start_time": "2026-07-14T10:00:00", "end_time": "2026-07-14T11:00:00"}
    assert CopilotActionRegistry.validate_inputs("create_calendar_event", payload)
