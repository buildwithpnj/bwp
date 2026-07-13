import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.telemetry_event import TelemetryEvent
from app.schemas.telemetry_event_schema import TelemetryEventCreate

class DistributedTelemetryService:
    @classmethod
    async def record_event(
        cls,
        db: AsyncSession,
        req: TelemetryEventCreate
    ) -> TelemetryEvent:
        """
        Saves distributed logging parameters.
        """
        event = TelemetryEvent(
            id=str(uuid.uuid4()),
            tenant_id=req.tenant_id,
            node_id=req.node_id,
            service_name=req.service_name,
            environment=req.environment,
            signal_type=req.signal_type,
            payload=req.payload
        )
        db.add(event)
        await db.commit()
        return event
