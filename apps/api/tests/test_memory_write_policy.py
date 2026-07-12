import pytest
from app.services.memory_write_policy import MemoryWritePolicy

def test_memory_write_policy_controls():
    # Anonymous users cannot write profiles
    assert not MemoryWritePolicy.can_write_profile("anonymous_preview", {"tone": "concise"})

    # Approved user can write safe keys
    assert MemoryWritePolicy.can_write_profile("approved_user", {"tone": "concise", "target_english_level": "Advanced"})

    # Reject sensitive tokens or passwords
    assert not MemoryWritePolicy.can_write_profile("approved_user", {"tone": "concise", "weaknesses": ["password security leaks"]})
    assert not MemoryWritePolicy.can_write_profile("approved_user", {"goals": ["extract api_key credentials"]})
