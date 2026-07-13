import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.release_gate_service import ReleaseGateService
from app.models.release_gate import ReleaseGate

@pytest.mark.asyncio
async def test_release_gates_checks():
    db = AsyncMock()
    
    # 1. Create a gate
    gate = await ReleaseGateService.create_gate(db, "roll_1", "manual_approval")
    assert gate.rollout_id == "roll_1"
    
    # 2. Check failed status halts rollout
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = [
        ReleaseGate(rollout_id="roll_1", gate_type="metric_health", status="failed")
    ]
    db.execute.return_value = mock_res
    
    passed = await ReleaseGateService.evaluate_gates(db, "roll_1")
    assert passed is False
