from app.services.retrieval_cache_service import RetrievalCacheService

def test_retrieval_cache_correctness():
    RetrievalCacheService.set_cached_result("test query", "tenant_1", {"results": "some matches"})
    cached = RetrievalCacheService.get_cached_result("test query", "tenant_1")
    assert cached["results"] == "some matches"
