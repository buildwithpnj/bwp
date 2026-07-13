import logging
import time
from typing import Dict, Any
from app.services.action_dispatcher import ActionDispatcher
from app.services.worker_health_service import WorkerHealthService

logger = logging.getLogger("metrics_worker")

class MetricsWorker:
    @classmethod
    async def collect_worker_metrics(cls) -> Dict[str, Any]:
        """
        Gathers queue depth, active worker counts, and heartbeat statuses.
        """
        adapter = ActionDispatcher.get_adapter()
        
        # Pull stats
        actions_depth = await adapter.size("actions")
        workflows_depth = await adapter.size("workflows")
        
        # Record heartbeats
        WorkerHealthService.record_heartbeat("memory_worker")
        
        stats = {
            "timestamp": time.time(),
            "queues": {
                "actions_depth": actions_depth,
                "workflows_depth": workflows_depth
            },
            "workers": WorkerHealthService.get_health_status()
        }
        
        logger.info(f"Worker Telemetry collected: {stats}")
        return stats
