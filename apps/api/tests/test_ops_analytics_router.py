import pytest
from unittest.mock import AsyncMock, MagicMock
from app.routers.ops_analytics_router import get_ops_risk_overview, schedule_prevention_review

@pytest.mark.asyncio
async def test_ops_analytics_router_endpoints():
    db = AsyncMock()
    
    admin_user = MagicMock()
    admin_user.role = "admin"
    
    # 1. Fetch risk overview
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res
    
    overview = await get_ops_risk_overview(admin_user, db)
    assert overview["risk_score"] == 0.12
    
    # 2. Schedule review
    res = await schedule_prevention_review("failure_spike", admin_user, db)
    assert res["status"] == "scheduled"
