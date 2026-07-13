import time
from typing import Dict, Any, Optional
from app.services.queue_adapter import QueueAdapter, MemoryQueueAdapter, QueueJob

class ActionDispatcher:
    _adapter: QueueAdapter = MemoryQueueAdapter()

    @classmethod
    def set_adapter(cls, adapter: QueueAdapter) -> None:
        cls._adapter = adapter

    @classmethod
    def get_adapter(cls) -> QueueAdapter:
        return cls._adapter

    @classmethod
    async def dispatch(
        cls,
        action_log_id: str,
        action_name: str,
        user_id: str,
        tenant_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        retry_count: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
        delay_seconds: int = 0
    ) -> str:
        """
        Dispatches an action job to the active queue.
        """
        run_at = time.time() + delay_seconds if delay_seconds > 0 else None
        
        meta = metadata or {}
        queue_name = meta.get("queue_name", "default")
        meta["queue_name"] = queue_name
        
        job = QueueJob(
            action_log_id=action_log_id,
            action_name=action_name,
            user_id=user_id,
            tenant_id=tenant_id,
            idempotency_key=idempotency_key,
            retry_count=retry_count,
            metadata=meta,
            run_at=run_at
        )
        
        job_id = await cls._adapter.enqueue(job)
        return job_id
