import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.anomaly_incident import AnomalyIncident
from app.schemas.anomaly_signal_schema import AnomalySignalSchema

class AnomalyDetectionService:
    @classmethod
    async def log_anomaly(
        cls,
        db: AsyncSession,
        req: AnomalySignalSchema
    ) -> AnomalyIncident:
        """
        Creates new anomaly occurrences logs.
        """
        incident = AnomalyIncident(
            id=str(uuid.uuid4()),
            tenant_id=req.tenant_id,
            signal_type=req.signal_type,
            severity=req.severity,
            incident_status="active",
            summary=req.summary
        )
        db.add(incident)
        await db.commit()
        return incident
