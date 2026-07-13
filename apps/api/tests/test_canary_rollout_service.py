import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.canary_rollout_service import CanaryRolloutService
from app.services.canary_scope_selector import CanaryScopeSelector
from app.services.rollout_stage_manager import RolloutStageManager
from app.models.canary_rollout import CanaryRollout

@pytest.mark.asyncio
async def test_canary_progression_rules():
    db = AsyncMock()
    
    # 1. Start canary
    canary = await CanaryRolloutService.initiate_rollout(db, "roll_123", 20)
    assert canary.canary_percentage == 20
    assert canary.status == "active"
    
    # 2. Scope target filtering
    nodes = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
    targets = CanaryScopeSelector.filter_canary_targets(nodes, 50)  # 50% = 2 nodes
    assert len(targets) == 2
    
    # 3. Stage transition mock
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = canary
    db.execute.return_value = mock_res
    
    paused = await RolloutStageManager.modify_rollout_status(db, "roll_123", "pause")
    assert paused.status == "paused"
