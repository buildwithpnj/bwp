import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.rollback_trigger_service import RollbackTriggerService
from app.models.canary_rollout import CanaryRollout

@pytest.mark.asyncio
async def test_auto_rollback_triggering():
    db = AsyncMock()
    
    canary = CanaryRollout(rollout_id="roll_1", status="active")
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = canary
    db.execute.return_value = mock_res
    
    # Health score 0.3 should trigger auto-rollback
    triggered = await RollbackTriggerService.evaluate_and_trigger(db, "roll_1", 0.3)
    assert triggered is True
    assert canary.status == "rolled_back"
    
    # Healthy score does not trigger rollback
    triggered_ok = await RollbackTriggerService.evaluate_and_trigger(db, "roll_1", 0.8)
    assert triggered_ok is False
