import pytest
from unittest.mock import AsyncMock
from app.services.collaboration_orchestrator import CollaborationOrchestrator
from app.schemas.collaboration_request import CollaborationRequest

@pytest.mark.asyncio
async def test_multi_agent_collaboration_run():
    db = AsyncMock()
    
    req = CollaborationRequest(
        workflow_run_id="wf_collab_123",
        participating_agents=["CodeReviewerAgent", "DatabaseAuditorAgent", "WorkflowDiagnosticianAgent"],
        max_steps=5
    )
    
    resp = await CollaborationOrchestrator.run_collaboration(db, req)
    
    assert resp.coordination_status == "merged"
    assert resp.handoffs_count == 2
    assert resp.used_tokens > 0.0
    assert "CodeReviewerAgent_to_DatabaseAuditorAgent" in resp.final_merged_result["findings_summary"]
    
    # Check db saves
    assert db.commit.call_count > 0
