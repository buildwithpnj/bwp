import pytest
from unittest.mock import AsyncMock
from app.services.distributed_telemetry_service import DistributedTelemetryService
from app.schemas.telemetry_event_schema import TelemetryEventCreate

@pytest.mark.asyncio
async def test_distributed_telemetry_event_logging():
    db = AsyncMock()
    req = TelemetryEventCreate(
        tenant_id="tenant_123",
        node_id="node_1",
        service_name="workflow_worker",
        environment="production",
        signal_type="log",
        payload="Workflow run finished with errors"
    )
    
    event = await DistributedTelemetryService.record_event(db, req)
    assert event.tenant_id == "tenant_123"
    assert event.signal_type == "log"
