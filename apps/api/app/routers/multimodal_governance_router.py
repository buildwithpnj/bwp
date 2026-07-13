from fastapi import APIRouter, status
from app.deps import CurrentUser, DB
from app.services.multimodal_quota_service import MultimodalQuotaService

router = APIRouter(prefix="/api/multimodal/governance", tags=["Multimodal Ingestion Governance"])

@router.get("/quota", status_code=status.HTTP_200_OK)
async def get_tenant_modality_quota(
    tenant_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Exposes active quota metrics, daily bytes used, and request frequency counts for a tenant.
    """
    quota = await MultimodalQuotaService.get_or_create_quota(db, tenant_id)
    return {
        "tenant_id": quota.tenant_id,
        "daily_bytes_limit": quota.daily_bytes_limit,
        "daily_bytes_used": quota.daily_bytes_used,
        "requests_count_limit": quota.requests_count_limit,
        "requests_count_used": quota.requests_count_used
    }
