from app.services.retrieval_quality_dashboard_service import RetrievalQualityDashboardService

def test_retrieval_observability_dashboard():
    res = RetrievalQualityDashboardService.compile_observability_data()
    assert "p95_latency_ms" in res
    assert res["grounding_audit_failure_rate"] < 0.05
