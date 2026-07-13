import pytest
from unittest.mock import AsyncMock, MagicMock
from app.routers.resilience_router import get_resilience_state, activate_degraded_mode
from app.models.resilience_state import ResilienceState

@pytest.mark.asyncio
async def test_resilience_router_endpoints():
    db = AsyncMock()
    
    admin_user = MagicMock()
    admin_user.role = "admin"
    
    # 1. Manually configure scope
    act = await activate_degraded_mode("analytics", "local_fallback", "simulations", admin_user, db)
    assert act.affected_scope == "analytics"
    
    # 2. Fetch state
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = ResilienceState(
        trigger_type="outage", affected_scope="all", degradation_level="critical"
    )
    db.execute.return_value = mock_res
    
    state = await get_resilience_state(admin_user, db)
    assert state.degradation_level == "critical"
