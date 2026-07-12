import pytest
from app.services.action_registry import ActionRegistry

def test_action_registry_validation():
    # Valid actions metadata retrieval
    assert "save_corrected_example" in ActionRegistry.list_actions()
    
    # Valid inputs schema checks
    payload = {"original": "me goes", "corrected": "I go", "explanation": "Grammar fix"}
    assert ActionRegistry.validate_inputs("save_corrected_example", payload)
    
    # Invalid payloads should fail schema checks
    bad_payload = {"original": "me goes", "corrected": 123}  # Wrong type
    assert not ActionRegistry.validate_inputs("save_corrected_example", bad_payload)
