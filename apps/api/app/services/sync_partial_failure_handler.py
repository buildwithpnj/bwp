import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.policy_sync_result import PolicySyncResult

class SyncPartialFailureHandler:
    @classmethod
    async def log_failure(
        cls,
        db: AsyncSession,
        target_id: str,
        error_msg: str
    ) -> PolicySyncResult:
        """
        Quarantines target failure outputs, saving healthy nodes from corruption.
        """
        result = PolicySyncResult(
            id=str(uuid.uuid4()),
            target_id=target_id,
            status="failed",
            error_message=error_msg
        )
        db.add(result)
        await db.commit()
        return result
