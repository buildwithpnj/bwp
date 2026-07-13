import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.release_approval_event import ReleaseApprovalEvent
from app.models.release_gate import ReleaseGate

class ReleaseApprovalService:
    @classmethod
    async def approve_release(
        cls,
        db: AsyncSession,
        rollout_id: str,
        user_id: str
    ) -> ReleaseApprovalEvent:
        """
        Registers admin approval event, updating pending gate status.
        """
        # Save approval event
        evt = ReleaseApprovalEvent(
            id=str(uuid.uuid4()),
            rollout_id=rollout_id,
            approved_by_user_id=user_id
        )
        db.add(evt)
        
        # Approve related gate if present
        stmt = select(ReleaseGate).where(
            ReleaseGate.rollout_id == rollout_id,
            ReleaseGate.gate_type == "manual_approval"
        )
        res = await db.execute(stmt)
        gate = res.scalar_one_or_none()
        if gate:
            gate.status = "passed"
            db.add(gate)
            
        await db.commit()
        return evt
