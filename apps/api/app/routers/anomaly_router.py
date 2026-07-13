from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.anomaly_incident import AnomalyIncident
import datetime

router = APIRouter(prefix="/api/anomalies", tags=["Anomaly Observability"])

@router.get("/incidents", status_code=status.HTTP_200_OK)
async def list_anomaly_incidents(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists current aggregated anomaly incidents.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(AnomalyIncident).order_by(AnomalyIncident.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/incidents/{incident_id}", status_code=status.HTTP_200_OK)
async def get_incident(
    incident_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Fetches details of a specific incident log.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(AnomalyIncident).where(AnomalyIncident.id == incident_id)
    res = await db.execute(stmt)
    incident = res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found."
        )
    return incident

@router.post("/incidents/{incident_id}/acknowledge", status_code=status.HTTP_200_OK)
async def acknowledge_incident(
    incident_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Marks anomaly incident state as acknowledged.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(AnomalyIncident).where(AnomalyIncident.id == incident_id)
    res = await db.execute(stmt)
    incident = res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found."
        )
        
    incident.incident_status = "acknowledged"
    db.add(incident)
    await db.commit()
    return incident

@router.post("/incidents/{incident_id}/resolve", status_code=status.HTTP_200_OK)
async def resolve_incident(
    incident_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Resolves active anomaly alerts.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(AnomalyIncident).where(AnomalyIncident.id == incident_id)
    res = await db.execute(stmt)
    incident = res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found."
        )
        
    incident.incident_status = "resolved"
    incident.resolved_at = datetime.datetime.now(datetime.timezone.utc)
    db.add(incident)
    await db.commit()
    return incident
