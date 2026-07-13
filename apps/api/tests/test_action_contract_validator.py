import pytest
from app.services.action_contract_validator import ActionContractValidator
from app.services.action_persistence_guard import ActionPersistenceGuard

def test_action_contract_validation_logic():
    # Valid note contract
    ok, err = ActionContractValidator.validate_action_contract(
        "create_note", {"title": "Test Title", "content": "Test Content"}
    )
    assert ok is True
    
    # Invalid note contract
    ok, err = ActionContractValidator.validate_action_contract(
        "create_note", {"title": 123, "content": "Test Content"}
    )
    assert ok is False
    assert "must be of type" in err
    
    # Missing parameter
    ok, err = ActionContractValidator.validate_action_contract(
        "create_note", {"title": "Test Title"}
    )
    assert ok is False
    assert "Missing required parameter" in err

def test_persistence_guard_logic():
    # Valid title
    ok, err = ActionPersistenceGuard.validate_write_safety(
        "create_note", {"title": "Valid Note", "content": ""}
    )
    assert ok is True
    
    # Empty title
    ok, err = ActionPersistenceGuard.validate_write_safety(
        "create_note", {"title": "   ", "content": ""}
    )
    assert ok is False
    assert "Title must contain" in err
    
    # Title too long
    ok, err = ActionPersistenceGuard.validate_write_safety(
        "create_note", {"title": "a" * 300, "content": ""}
    )
    assert ok is False
    assert "exceeds 255" in err
