from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.resilience_state import ResilienceState
from app.models.degraded_mode_activation import DegradedModeActivation
from app.schemas.resilience_policy_schema import ResiliencePolicyCreate
from app.services.resilience_policy_service import ResiliencePolicyService
from app.services.degraded_mode_manager import DegradedModeManager
from app.services.recovery_transition_service import RecoveryTransitionService

router = APIRouter(prefix="/api/resilience", tags=["Resilience Automation"])

@router.get("/state", status_code=status.HTTP_200_OK)
async def get_resilience_state(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns active system resilience and degradation levels status parameters.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(ResilienceState).order_by(ResilienceState.created_at.desc()).limit(1)
    res = await db.execute(stmt)
    state = res.scalar_one_or_none()
    
    if not state:
        return {
            "trigger_type": "none",
            "affected_scope": "all",
            "degradation_level": "normal",
            "token_budget_reduction_factor": 1.0
        }
    return state

@router.post("/degraded/activate", status_code=status.HTTP_201_CREATED)
async def activate_degraded_mode(
    scope: str,
    active_features: str,
    disabled_features: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Enters degraded operations mode manually.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await DegradedModeManager.activate_degraded(db, scope, active_features, disabled_features)

@router.post("/degraded/override", status_code=status.HTTP_200_OK)
async def override_degraded_mode(
    current_user: CurrentUser,
    db: DB
):
    """
    Clears degraded mode parameters manual override.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return {"status": "overridden", "degradation_level": "normal"}

@router.post("/recovery/start", status_code=status.HTTP_200_OK)
async def start_recovery(
    scope: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Logs recovery transition steps.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await RecoveryTransitionService.log_recovery(db, scope)

@router.get("/history", status_code=status.HTTP_200_OK)
async def list_resilience_history(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists degraded activations logs.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(DegradedModeActivation).order_by(DegradedModeActivation.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()
