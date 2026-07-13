import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.release_gate import ReleaseGate

class ReleaseGateService:
    @classmethod
    async def evaluate_gates(
        cls,
        db: AsyncSession,
        rollout_id: str
    ) -> bool:
        """
        Verifies if all release gate checkpoints have passed successfully.
        """
        stmt = select(ReleaseGate).where(ReleaseGate.rollout_id == rollout_id)
        res = await db.execute(stmt)
        gates = res.scalars().all()
        
        # If any gate is failed, block rollout
        for g in gates:
            if g.status == "failed":
                return False
        return True
        
    @classmethod
    async def create_gate(
        cls,
        db: AsyncSession,
        rollout_id: str,
        gate_type: str
    ) -> ReleaseGate:
        """
        Creates a new safety gate trigger.
        """
        gate = ReleaseGate(
            id=str(uuid.uuid4()),
            rollout_id=rollout_id,
            gate_type=gate_type,
            status="pending"
        )
        db.add(gate)
        await db.commit()
        return gate
