import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.governance_policy_service import GovernancePolicyService
from app.schemas.governance_update_request import GovernanceUpdateRequest
from app.services.tenant_agent_config_service import TenantAgentConfigService
from app.services.tenant_alert_rule_service import TenantAlertRuleService
from app.services.governance_audit_service import GovernanceAuditService

@pytest.mark.asyncio
async def test_operational_governance_policing():
    db = AsyncMock()
    
    # 1. Update config toggle
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res
    
    policy = await TenantAgentConfigService.configure_agent_availability(db, "tenant_1", "research", False)
    assert policy.is_enabled is False
    
    # 2. Toggle alert rule muting
    mock_res2 = MagicMock()
    mock_res2.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res2
    
    rule = await TenantAlertRuleService.configure_alert_muting(db, "tenant_1", "quota_warning", True)
    assert rule.is_muted is True
    
    # 3. Log governance audit change log
    data = GovernanceUpdateRequest(tenant_id="tenant_1", field_name="modality_limit", new_value="50000000")
    change = await GovernancePolicyService.log_policy_change(db, "admin_user", data, "25000000")
    assert change.old_value == "25000000"
    
    # 4. Fetch history list
    mock_history = MagicMock()
    mock_history.scalars.return_value.all.return_value = [change]
    db.execute.return_value = mock_history
    
    history = await GovernanceAuditService.get_revision_history(db, "tenant_1")
    assert len(history) == 1
    assert history[0].field_name == "modality_limit"
