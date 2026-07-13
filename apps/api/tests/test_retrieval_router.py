import pytest
from unittest.mock import AsyncMock, MagicMock
from app.routers.retrieval_router import query_knowledge_base, submit_feedback
from app.schemas.retrieval_request_schema import RetrievalRequestSchema

@pytest.mark.asyncio
async def test_retrieval_router_queries():
    db = AsyncMock()
    
    admin_user = MagicMock()
    admin_user.role = "admin"
    admin_user.tenant_id = "tenant_123"
    
    req = RetrievalRequestSchema(
        query="active configurations",
        tenant_id="tenant_123",
        page_scope="dashboard"
    )
    
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = []
    db.execute.return_value = mock_res
    
    res = await query_knowledge_base(req, admin_user, db)
    assert res.query_text == "active configurations"
    assert res.strategy_used == "hybrid_keyword_vector"
