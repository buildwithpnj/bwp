import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class QueueJob:
    def __init__(
        self,
        action_log_id: str,
        action_name: str,
        user_id: str,
        tenant_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        retry_count: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
        run_at: Optional[float] = None
    ):
        self.job_id = str(uuid.uuid4())
        self.action_log_id = action_log_id
        self.action_name = action_name
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.idempotency_key = idempotency_key
        self.retry_count = retry_count
        self.metadata = metadata or {}
        self.run_at = run_at  # Epoch timestamp when job is eligible to run

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "action_log_id": self.action_log_id,
            "action_name": self.action_name,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "idempotency_key": self.idempotency_key,
            "retry_count": self.retry_count,
            "metadata": self.metadata,
            "run_at": self.run_at
        }

class QueueAdapter(ABC):
    @abstractmethod
    async def enqueue(self, job: QueueJob) -> str:
        pass

    @abstractmethod
    async def dequeue(self, queue_name: str) -> Optional[QueueJob]:
        pass

    @abstractmethod
    async def size(self, queue_name: str) -> int:
        pass

    @abstractmethod
    async def clear(self, queue_name: str) -> None:
        pass

class MemoryQueueAdapter(QueueAdapter):
    _queues: Dict[str, List[QueueJob]] = {}
    _lock = asyncio.Lock()

    @classmethod
    def get_queue(cls, queue_name: str) -> List[QueueJob]:
        if queue_name not in cls._queues:
            cls._queues[queue_name] = []
        return cls._queues[queue_name]

    async def enqueue(self, job: QueueJob) -> str:
        async with self._lock:
            q = self.get_queue(job.metadata.get("queue_name", "default"))
            q.append(job)
            return job.job_id

    async def dequeue(self, queue_name: str) -> Optional[QueueJob]:
        async with self._lock:
            q = self.get_queue(queue_name)
            if not q:
                return None
            
            # Find eligible jobs based on run_at
            now = time.time()
            for idx, job in enumerate(q):
                if job.run_at is None or job.run_at <= now:
                    return q.pop(idx)
                    
            return None

    async def size(self, queue_name: str) -> int:
        async with self._lock:
            return len(self.get_queue(queue_name))

    async def clear(self, queue_name: str) -> None:
        async with self._lock:
            if queue_name in self._queues:
                self._queues[queue_name].clear()
