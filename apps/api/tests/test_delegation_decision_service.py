import pytest
from unittest.mock import AsyncMock
from app.services.delegation_decision_service import DelegationDecisionService
from app.services.specialist_delegation_policy import SpecialistDelegationPolicy

@pytest.mark.asyncio
async def test_delegation_decision_routing():
    db = AsyncMock()
    SpecialistDelegationPolicy.reset_policy_limits()
    
    # 1. SQLite schema error should route to DatabaseAuditorAgent
    agent = await DelegationDecisionService.evaluate_and_route(
        db, "wf_1", "Operational database query failure: sqlite foreign key violation", 0
    )
    assert agent == "DatabaseAuditorAgent"
    
    # 2. Syntax/Indentation errors should route to CodeReviewerAgent
    agent_code = await DelegationDecisionService.evaluate_and_route(
        db, "wf_1", "Compilation crash: SyntaxError invalid syntax", 0
    )
    assert agent_code == "CodeReviewerAgent"
    
    # 3. High retries should route to WorkflowDiagnosticianAgent
    agent_retry = await DelegationDecisionService.evaluate_and_route(
        db, "wf_1", "Uncaught exception", 2
    )
    assert agent_retry == "WorkflowDiagnosticianAgent"
