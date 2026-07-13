import pytest
from unittest.mock import AsyncMock
from app.services.anomaly_detection_service import AnomalyDetectionService
from app.schemas.anomaly_signal_schema import AnomalySignalSchema
from app.services.anomaly_severity_service import AnomalySeverityService
from app.services.anomaly_dedup_service import AnomalyDedupService
from app.services.anomaly_thread_integration_service import AnomalyThreadIntegrationService
from app.services.anomaly_recommendation_service import AnomalyRecommendationService

@pytest.mark.asyncio
async def test_anomaly_incident_evaluation():
    db = AsyncMock()
    
    # 1. Logging
    req = AnomalySignalSchema(
        tenant_id="tenant_1",
        signal_type="quota_breach",
        severity="medium",
        summary="Quota usage warning"
    )
    incident = await AnomalyDetectionService.log_anomaly(db, req)
    assert incident.signal_type == "quota_breach"
    
    # 2. Severity levels evaluation
    assert AnomalySeverityService.evaluate_severity(12) == "critical"
    assert AnomalySeverityService.evaluate_severity(5) == "high"
    assert AnomalySeverityService.evaluate_severity(2) == "medium"
    
    # 3. Deduplication check
    assert AnomalyDedupService.is_duplicate(["key_1", "key_2"], "key_1") is True
    assert AnomalyDedupService.is_duplicate(["key_1", "key_2"], "key_3") is False
    
    # 4. Thread link and preventive suggestions
    link = AnomalyThreadIntegrationService.link_to_thread("thread_1", incident.id)
    assert link["linked"] is True
    
    recs = AnomalyRecommendationService.get_recommendations("quota_breach")
    assert "increase_limit" in recs
