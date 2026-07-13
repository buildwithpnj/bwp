import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.policy_sync_job import PolicySyncJob
from app.schemas.policy_sync_request import PolicySyncRequest
from app.services.sync_signature_service import SyncSignatureService
from app.services.policy_sync_executor import PolicySyncExecutor
from app.services.federated_sync_scope_service import FederatedSyncScopeService

class GovernanceSyncService:
    @classmethod
    async def process_sync(
        cls,
        db: AsyncSession,
        user_id: str,
        req: PolicySyncRequest
    ) -> PolicySyncJob:
        """
        Processes multi-node configurations, ensuring signature validity.
        """
        # Validate signed code
        if not SyncSignatureService.verify_signature(req.source_env + req.target_env, req.signature):
            raise ValueError("Cryptographic verification failed.")
            
        job = PolicySyncJob(
            id=str(uuid.uuid4()),
            user_id=user_id,
            source_env=req.source_env,
            target_env=req.target_env,
            status="applied",
            signature=req.signature
        )
        db.add(job)
        
        # Build scopes
        targets = FederatedSyncScopeService.filter_targets(req.target_nodes, req.target_tenants)
        await PolicySyncExecutor.execute_sync(db, job.id, targets)
        
        await db.commit()
        return job
