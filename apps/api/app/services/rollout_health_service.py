import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rollout_health_snapshot import RolloutHealthSnapshot

class RolloutHealthService:
    @classmethod
    async def measure_health(
        cls,
        db: AsyncSession,
        rollout_id: str,
        failure_rate: float,
        latency_delta: float
    ) -> RolloutHealthSnapshot:
        """
        Assesses rollout telemetry data. Health decreases if failure rate > 0.05.
        """
        score = 1.0
        summary = "Rollout is healthy."
        
        if failure_rate > 0.05 or latency_delta > 500:
            score = 0.4
            summary = "Unhealthy: high latency delta or failure spike."
            
        snap = RolloutHealthSnapshot(
            id=str(uuid.uuid4()),
            rollout_id=rollout_id,
            health_score=score,
            status_summary=summary
        )
        db.add(snap)
        await db.commit()
        return snap
