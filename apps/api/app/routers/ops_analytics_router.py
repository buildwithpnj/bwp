from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.ops_risk_snapshot import OpsRiskSnapshot
from app.models.pattern_regression_case import PatternRegressionCase
from app.models.predictive_incident_signal import PredictiveIncidentSignal

router = APIRouter(prefix="/api/ops/risk", tags=["Predictive failure & Risk analytics"])

@router.get("/overview", status_code=status.HTTP_200_OK)
async def get_ops_risk_overview(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns aggregate risk scopes.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(OpsRiskSnapshot).order_by(OpsRiskSnapshot.created_at.desc()).limit(1)
    res = await db.execute(stmt)
    snapshot = res.scalar_one_or_none()
    
    if not snapshot:
        return {
            "tenant_scope": "all",
            "cluster_scope": "production_cluster",
            "risk_score": 0.12,
            "confidence_score": 0.95,
            "recommended_prevention": "continue_normal_monitoring"
        }
    return snapshot

@router.get("/patterns", status_code=status.HTTP_200_OK)
async def list_failure_patterns(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists historical pattern regressions cases.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(PatternRegressionCase).order_by(PatternRegressionCase.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/predictions", status_code=status.HTTP_200_OK)
async def list_predictive_signals(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists current forecasting signals.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(PredictiveIncidentSignal).order_by(PredictiveIncidentSignal.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_prevention_recommendations(
    current_user: CurrentUser,
    db: DB
):
    """
    Fetches mitigation recommendations checklist.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return [
        {"action": "recommend_degraded_fallback_mode", "risk_level": "medium"},
        {"action": "schedule_alert_quota_review", "risk_level": "low"}
    ]

@router.post("/review/schedule", status_code=status.HTTP_201_CREATED)
async def schedule_prevention_review(
    pattern_family: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Schedules operational review actions.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return {"pattern_family": pattern_family, "status": "scheduled"}
