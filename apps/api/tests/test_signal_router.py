import pytest
from unittest.mock import AsyncMock
from app.services.signal_router import SignalRouter
from app.schemas.normalized_signal_schema import NormalizedSignal

@pytest.mark.asyncio
async def test_signal_to_workflow_blueprints():
    db = AsyncMock()
    
    # 1. create_lesson_note routing blueprint
    sig = NormalizedSignal(
        media_type="document",
        extracted_text="Some document lesson note content.",
        suggested_workflow_type="create_lesson_note"
    )
    blueprint = await SignalRouter.route_signal_to_workflow(db, sig)
    assert blueprint["suggested_workflow_type"] == "create_lesson_note"
    assert blueprint["steps"][0]["action_name"] == "create_lesson_note"
    assert blueprint["requires_approval"] is False
    
    # 2. build_practice_plan routing blueprint
    sig_practice = NormalizedSignal(
        media_type="screenshot",
        extracted_text="Some practice screenshot details.",
        suggested_workflow_type="build_practice_plan"
    )
    blueprint_practice = await SignalRouter.route_signal_to_workflow(db, sig_practice)
    assert blueprint_practice["suggested_workflow_type"] == "build_practice_plan"
    assert blueprint_practice["steps"][0]["action_name"] == "build_practice_plan"
    assert blueprint_practice["requires_approval"] is True
