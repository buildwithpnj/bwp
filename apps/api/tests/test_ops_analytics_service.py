import pytest
from unittest.mock import AsyncMock
from app.services.cross_tenant_analytics_service import CrossTenantAnalyticsService
from app.services.pattern_detection_service import PatternDetectionService
from app.services.predictive_risk_service import PredictiveRiskService
from app.schemas.ops_risk_schema import OpsRiskCreate
from app.services.failure_forecast_service import FailureForecastService
from app.services.prediction_explainability_service import PredictionExplainabilityService
from app.services.preventive_recommendation_service import PreventiveRecommendationService
from app.services.risk_threshold_policy_service import RiskThresholdPolicyService
from app.services.preventive_notification_service import PreventiveNotificationService
from app.services.ops_review_scheduler import OpsReviewScheduler

@pytest.mark.asyncio
async def test_predictive_risk_forecasting():
    db = AsyncMock()
    
    # 1. Anonymous Cross-Tenant Aggregations
    rate = CrossTenantAnalyticsService.aggregate_anonymous_metrics([
        {"failure_rate": 0.02},
        {"failure_rate": 0.08}
    ])
    assert rate == 0.05
    
    # 2. Risk Snapshot Logging
    req = OpsRiskCreate(
        tenant_scope="tenant_abc",
        cluster_scope="prod_cluster",
        risk_score=0.85,
        confidence_score=0.92,
        recommended_prevention="throttle_runs"
    )
    snap = await PredictiveRiskService.evaluate_risk(db, req)
    assert snap.risk_score == 0.85
    
    # 3. Forecast trend
    assert FailureForecastService.forecast_failure_probability(150.0, 0.08) == 0.75
    
    # 4. Explainability & Preventive Suggestion
    expl = PredictionExplainabilityService.generate_explanation(0.85)
    assert "High risk" in expl
    
    recs = PreventiveRecommendationService.generate_recommendation(0.85)
    assert recs == "recommend_degraded_fallback_mode"
    
    assert RiskThresholdPolicyService.check_threshold_breach(0.85) is True
    
    alert = PreventiveNotificationService.format_alert(0.85, "prod_cluster")
    assert "85%" in alert
    
    # 5. Review schedules
    task = OpsReviewScheduler.schedule_review("quota_spike")
    assert task["status"] == "scheduled"
