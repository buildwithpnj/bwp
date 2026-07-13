import pytest
from unittest.mock import AsyncMock
from app.services.rollout_health_service import RolloutHealthService

@pytest.mark.asyncio
async def test_health_evaluation_limits():
    db = AsyncMock()
    
    # 1. Healthy run
    snap = await RolloutHealthService.measure_health(db, "roll_1", 0.02, 100.0)
    assert snap.health_score == 1.0
    
    # 2. Unhealthy spike
    snap_fail = await RolloutHealthService.measure_health(db, "roll_1", 0.08, 100.0)
    assert snap_fail.health_score == 0.4
