import pytest
from app.services.failure_pattern_service import FailurePatternService
from app.models.action_models import ActionLog

def test_analyze_patterns_retry_and_timeout():
    log = ActionLog(
        id="log_1",
        user_id="user_1",
        action_name="create_lesson_note",
        retry_count=2,
        error_message="Gateway Timeout exception"
    )
    
    patterns = FailurePatternService.analyze_patterns(log)
    assert "repeated_retry_pattern" in patterns
    assert "timeout_pattern" in patterns
