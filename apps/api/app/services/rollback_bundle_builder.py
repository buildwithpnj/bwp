import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.federated_rollback_bundle import FederatedRollbackBundle

class RollbackBundleBuilder:
    @classmethod
    async def build_bundle(
        cls,
        db: AsyncSession,
        job_id: str,
        current_state: dict
    ) -> FederatedRollbackBundle:
        """
        Creates rollback state snapshots before executing sync policies.
        """
        bundle = FederatedRollbackBundle(
            id=str(uuid.uuid4()),
            job_id=job_id,
            snapshot_data=json.dumps(current_state)
        )
        db.add(bundle)
        await db.commit()
        return bundle
