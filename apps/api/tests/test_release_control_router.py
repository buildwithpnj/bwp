import pytest
from unittest.mock import AsyncMock, MagicMock
from app.routers.release_control_router import create_release_plan, start_canary
from app.schemas.release_plan_schema import ReleasePlanCreate

@pytest.mark.asyncio
async def test_release_router_gating():
    db = AsyncMock()
    
    # 1. Admin auth simulation
    admin_user = MagicMock()
    admin_user.role = "admin"
    admin_user.id = "admin_1"
    
    non_admin = MagicMock()
    non_admin.role = "user"
    
    plan = ReleasePlanCreate(
        rollout_id="roll_123",
        release_type="policy_change",
        target_scope="production",
        canary_percentage=10,
        approval_required=True
    )
    
    # Non-admin triggers error
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        await create_release_plan(plan, non_admin, db)
        
    # Admin starts canary rollout
    canary = await create_release_plan(plan, admin_user, db)
    assert canary is not None
