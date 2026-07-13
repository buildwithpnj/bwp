import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops_risk_snapshot import OpsRiskSnapshot
from app.schemas.ops_risk_schema import OpsRiskCreate

class PredictiveRiskService:
    @classmethod
    async def evaluate_risk(
        cls,
        db: AsyncSession,
        req: OpsRiskCreate
    ) -> OpsRiskSnapshot:
        """
        Stores predicted failure probability metrics.
        """
        snap = OpsRiskSnapshot(
            id=str(uuid.uuid4()),
            tenant_scope=req.tenant_scope,
            cluster_scope=req.cluster_scope,
            risk_score=req.risk_score,
            confidence_score=req.confidence_score,
            recommended_prevention=req.recommended_prevention
        )
        db.add(snap)
        await db.commit()
        return snap
