import pytest
from unittest.mock import AsyncMock
from app.services.recovery_suggestion_service import RecoverySuggestionService
from app.models.workflow_run import WorkflowRun
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_recovery_suggestion_generation():
    db = AsyncMock()
    wf = WorkflowRun(id="wf_1", steps=[], current_step_index=0)
    log = ActionLog(id="log_1")
    
    # 1. Test normal execution failure
    options = await RecoverySuggestionService.generate_and_rank_suggestions(db, wf, log, [])
    assert len(options) == 2
    assert options[0].action_type == "replay_failed_step"
    assert options[1].action_type == "cancel_workflow"
    
    # 2. Test repeated retry failure pattern
    options_retry = await RecoverySuggestionService.generate_and_rank_suggestions(db, wf, log, ["repeated_retry_pattern"])
    assert len(options_retry) == 2
    assert options_retry[0].action_type == "cancel_workflow"
    assert options_retry[1].action_type == "escalate_to_admin"
