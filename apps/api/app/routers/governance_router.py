from fastapi import APIRouter, HTTPException, status
from app.deps import CurrentUser, DB
from app.schemas.governance_update_request import GovernanceUpdateRequest
from app.services.governance_policy_service import GovernancePolicyService
from app.services.governance_audit_service import GovernanceAuditService
from app.services.tenant_agent_config_service import TenantAgentConfigService
from app.services.tenant_alert_rule_service import TenantAlertRuleService

router = APIRouter(prefix="/api/governance", tags=["Operational Governance Plane"])

@router.post("/log-policy", status_code=status.HTTP_201_CREATED)
async def update_governance_policy(
    data: GovernanceUpdateRequest,
    current_user: CurrentUser,
    db: DB
):
    """
    Saves and registers policy field updates with validation trails.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await GovernancePolicyService.log_policy_change(db, current_user.id, data, "original_baseline_value")

@router.get("/audit-trail", status_code=status.HTTP_200_OK)
async def get_audit_trail(
    tenant_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Fetches revision history list.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await GovernanceAuditService.get_revision_history(db, tenant_id)

@router.post("/configure-agent", status_code=status.HTTP_200_OK)
async def toggle_agent_policy(
    tenant_id: str,
    agent_type: str,
    enabled: bool,
    current_user: CurrentUser,
    db: DB
):
    """
    Enables/disables a specialized subagent for this tenant.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await TenantAgentConfigService.configure_agent_availability(db, tenant_id, agent_type, enabled)

@router.post("/configure-alert", status_code=status.HTTP_200_OK)
async def toggle_alert_muting(
    tenant_id: str,
    rule_name: str,
    muted: bool,
    current_user: CurrentUser,
    db: DB
):
    """
    Mutes/unmutes notification rules for this tenant.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await TenantAlertRuleService.configure_alert_muting(db, tenant_id, rule_name, muted)

@router.get("/approvals", status_code=status.HTTP_200_OK)
async def list_approvals(
    current_user: CurrentUser,
    db: DB,
    approval_status: str = None
):
    """
    Retrieves all action approval requests.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
    from sqlalchemy import select
    from app.models.action_approval_models import ActionApprovalRequest
    stmt = select(ActionApprovalRequest)
    if approval_status:
        stmt = stmt.where(ActionApprovalRequest.status == approval_status)
    stmt = stmt.order_by(ActionApprovalRequest.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/approvals/metrics", status_code=status.HTTP_200_OK)
async def get_approval_metrics(
    current_user: CurrentUser
):
    """
    Retrieves execution approval telemetry and counts.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
    from app.services.approval_metrics_service import ApprovalMetricsService
    return ApprovalMetricsService.get_metrics()
