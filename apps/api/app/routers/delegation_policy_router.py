from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import CurrentUser, DB
from app.models.delegation_policy_feedback import DelegationPolicyFeedback
from app.services.policy_rollback_service import PolicyRollbackService

router = APIRouter(prefix="/api/delegation/policy", tags=["Adaptive Delegation Policy"])

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def record_policy_feedback(
    specialist_type: str,
    workflow_type: str,
    usefulness_score: float,
    current_user: CurrentUser,
    db: DB
):
    """
    Submits evaluation feedback on specialist delegation efficiency to train adaptive thresholds.
    """
    feedback = DelegationPolicyFeedback(
        specialist_type=specialist_type,
        workflow_type=workflow_type,
        usefulness_score=usefulness_score
    )
    db.add(feedback)
    await db.commit()
    return {"status": "recorded"}

@router.post("/rollback", status_code=status.HTTP_200_OK)
async def rollback_delegation_policy(
    specialist_type: str,
    workflow_type: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Resets dynamic adaptive adjustments and restores standard configuration defaults for an agent. Gated to internal_admin.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to internal_admin."
        )
        
    await PolicyRollbackService.rollback_policy(db, specialist_type, workflow_type)
    return {"status": "rolled_back"}
