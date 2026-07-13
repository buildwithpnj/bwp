import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.hybrid_retrieval_service import HybridRetrievalService
from app.services.query_rewrite_service import QueryRewriteService
from app.services.metadata_filter_builder import MetadataFilterBuilder

@pytest.mark.asyncio
async def test_hybrid_retrieval_flow():
    db = AsyncMock()
    
    # 1. Query Expansion Check
    assert QueryRewriteService.expand_query("sync") == "sync policy synchronization cluster drift"
    
    # 2. Metadata Filtering Check
    filters = MetadataFilterBuilder.build_tenant_filters("tenant_123", "internal")
    assert filters["tenant_id"] == "tenant_123"
    
    # 3. Hybrid search candidates return check
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = []
    db.execute.return_value = mock_res
    
    results = await HybridRetrievalService.retrieve(db, "tenant_123", "policy sync")
    assert len(results) == 0
