from fastapi import APIRouter, HTTPException, Depends, status
from app.deps import CurrentUser
from app.services.action_metrics_service import ActionMetricsService

router = APIRouter(prefix="/api/actions/metrics", tags=["Action Metrics"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_metrics(current_user: CurrentUser):
    """
    Retrieves in-memory system metrics for action executions.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )
    return ActionMetricsService.get_summary()
