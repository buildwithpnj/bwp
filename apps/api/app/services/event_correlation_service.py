import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.anomaly_correlation_link import AnomalyCorrelationLink

class EventCorrelationService:
    @classmethod
    async def correlate_incidents(
        cls,
        db: AsyncSession,
        parent_id: str,
        child_id: str
    ) -> AnomalyCorrelationLink:
        """
        Links related anomalies to mitigate noise storms.
        """
        link = AnomalyCorrelationLink(
            id=str(uuid.uuid4()),
            parent_incident_id=parent_id,
            child_incident_id=child_id
        )
        db.add(link)
        await db.commit()
        return link
