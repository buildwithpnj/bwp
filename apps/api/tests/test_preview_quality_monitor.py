import pytest
from app.services.preview_quality_monitor import PreviewQualityMonitor
from app.services.preview_failure_bucket import PreviewFailureBucket

def test_response_monitoring():
    PreviewQualityMonitor._scores.clear()
    PreviewQualityMonitor._failures.clear()
    
    # 1. Valid responses
    score1 = PreviewQualityMonitor.monitor_response("sess1", "hello", "This is a clean and professional response.")
    assert score1 == 1.0
    
    # 2. Repeated word response (failed quality)
    bad_msg = "bad bad bad bad bad bad bad bad bad bad bad bad bad"
    score2 = PreviewQualityMonitor.monitor_response("sess2", "hello", bad_msg)
    assert score2 == 0.0
    
    stats = PreviewQualityMonitor.get_quality_stats()
    assert stats["pass_rate_percentage"] == 50.0
    assert stats["failure_count"] == 1
    
    # Bucket check
    buckets = PreviewFailureBucket.get_bucketed_failures()
    assert len(buckets["general_low_quality"]) == 1
