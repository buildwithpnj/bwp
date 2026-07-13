import pytest
from unittest.mock import AsyncMock
from app.services.handoff_protocol_service import HandoffProtocolService

@pytest.mark.asyncio
async def test_handoff_protocol_pathways_and_contracts():
    db = AsyncMock()
    
    # 1. Authorized Pathway & Valid contract
    success = await HandoffProtocolService.process_handoff(
        db, "col_1", "CodeReviewerAgent", "DatabaseAuditorAgent", {"code_findings": "Syntax error"}
    )
    assert success is True
    
    # 2. Authorized Pathway but Invalid contract (missing code_findings / anomaly_detected)
    success_invalid = await HandoffProtocolService.process_handoff(
        db, "col_1", "CodeReviewerAgent", "DatabaseAuditorAgent", {"something_else": "junk"}
    )
    assert success_invalid is False
    
    # 3. Unauthorized Pathway
    success_unauthorized = await HandoffProtocolService.process_handoff(
        db, "col_1", "CodeReviewerAgent", "SafetyPolicyCheckerAgent", {}
    )
    assert success_unauthorized is False
