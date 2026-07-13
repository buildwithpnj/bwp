import pytest
from unittest.mock import AsyncMock, MagicMock
from app.routers.anomaly_router import list_anomaly_incidents, resolve_incident
from app.models.anomaly_incident import AnomalyIncident

@pytest.mark.asyncio
async def test_anomaly_router_endpoints():
    db = AsyncMock()
    
    admin_user = MagicMock()
    admin_user.role = "admin"
    
    incident = AnomalyIncident(id="inc_123", tenant_id="tenant_1", signal_type="log_error", summary="Alert")
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = incident
    mock_res.scalars.return_value.all.return_value = [incident]
    db.execute.return_value = mock_res
    
    # 1. Fetch listing
    list_res = await list_anomaly_incidents(admin_user, db)
    assert len(list_res) == 1
    
    # 2. Resolve incident
    res = await resolve_incident("inc_123", admin_user, db)
    assert res.incident_status == "resolved"
