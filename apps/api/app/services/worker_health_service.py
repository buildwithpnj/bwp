import time
from typing import Dict, Any

class WorkerHealthService:
    # In-memory store for worker heartbeat timestamps
    _heartbeats: Dict[str, float] = {}

    @classmethod
    def record_heartbeat(cls, worker_id: str) -> None:
        """Saves current epoch timestamp for a given worker ID."""
        cls._heartbeats[worker_id] = time.time()

    @classmethod
    def get_health_status(cls) -> Dict[str, Any]:
        """
        Determines worker health status: workers are considered active
        if their last heartbeat is within 30 seconds.
        """
        now = time.time()
        active_workers = []
        stale_workers = []
        
        for w_id, last_seen in cls._heartbeats.items():
            if now - last_seen <= 30.0:
                active_workers.append(w_id)
            else:
                stale_workers.append(w_id)
                
        return {
            "active_workers": active_workers,
            "stale_workers": stale_workers,
            "worker_heartbeats": dict(cls._heartbeats)
        }
        
    @classmethod
    def reset_health(cls) -> None:
        cls._heartbeats.clear()
