import pytest
from unittest.mock import AsyncMock
from app.services.subagent_execution_service import SubAgentExecutionService
from app.schemas.delegation_request_schema import DelegationRequest
from app.services.specialist_delegation_policy import SpecialistDelegationPolicy

@pytest.mark.asyncio
async def test_subagent_delegation_execution():
    db = AsyncMock()
    SpecialistDelegationPolicy.reset_policy_limits()
    
    req = DelegationRequest(
        delegation_id="del_abc",
        workflow_run_id="wf_123",
        requesting_agent="PrimaryOrchestrator",
        specialist_type="DatabaseAuditorAgent",
        delegation_reason="FK Constraint issue",
        bounded_goal="Verify SQLite tables schema mapping consistency."
    )
    
    resp = await SubAgentExecutionService.execute_delegation(db, req)
    
    assert resp.delegation_id == "del_abc"
    assert resp.specialist_type == "DatabaseAuditorAgent"
    assert resp.outcome_status == "succeeded"
    assert resp.structured_findings["anomaly_detected"] is True
    assert resp.suggested_next_step["action"] == "escalate_to_admin"
    
    # Verify DB save was called
    db.add.assert_called_once()
