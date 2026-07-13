from fastapi import APIRouter, HTTPException, Depends, status
from app.deps import CurrentUser
from app.services.action_dispatcher import ActionDispatcher
from app.services.worker_health_service import WorkerHealthService
from app.services.action_metrics_service import ActionMetricsService

router = APIRouter(prefix="/api/actions/admin/worker/metrics", tags=["Action Worker Metrics"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_worker_metrics(current_user: CurrentUser):
    """
    Exposes queue sizes, heartbeats, and worker performance parameters.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )
        
    adapter = ActionDispatcher.get_adapter()
    actions_depth = await adapter.size("actions")
    workflows_depth = await adapter.size("workflows")
    
    summary = ActionMetricsService.get_summary()
    health = WorkerHealthService.get_health_status()
    
    return {
        "queue_depths": {
            "actions": actions_depth,
            "workflows": workflows_depth
        },
        "heartbeats": health,
        "counters": summary.get("counters", {}),
        "rates": summary.get("rates", {}),
        "averages": summary.get("averages", {})
    }
