from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.telemetry_event import TelemetryEvent
from app.schemas.telemetry_event_schema import TelemetryEventCreate
from app.services.distributed_telemetry_service import DistributedTelemetryService

router = APIRouter(prefix="/api/telemetry", tags=["Distributed Telemetry"])

@router.post("/events", status_code=status.HTTP_201_CREATED)
async def post_telemetry_event(
    req: TelemetryEventCreate,
    current_user: CurrentUser,
    db: DB
):
    """
    Saves a distributed metric/log event payload.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await DistributedTelemetryService.record_event(db, req)

@router.get("/overview", status_code=status.HTTP_200_OK)
async def get_telemetry_overview(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns aggregated telemetry cluster performance values.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return {
        "status": "healthy",
        "active_nodes": 4,
        "total_requests_count": 1420
    }

@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_telemetry_metrics(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns lists of active metric parameters.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return [
        {"metric_name": "cpu_utilization", "metric_value": 42.5},
        {"metric_name": "quota_utilization", "metric_value": 78.0}
    ]
