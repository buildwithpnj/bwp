import pytest
from app.services.telemetry_normalizer import TelemetryNormalizer
from app.services.metric_rollup_service import MetricRollupService
from app.services.log_signal_extractor import LogSignalExtractor

def test_telemetry_helpers():
    # 1. Normalizer cleanup
    assert TelemetryNormalizer.normalize_signal("  ERROR_LOG  ") == "error_log"
    
    # 2. Metric Rollup calculation
    assert MetricRollupService.calculate_rollup_average([10.0, 20.0, 30.0]) == 20.0
    assert MetricRollupService.calculate_rollup_average([]) == 0.0
    
    # 3. Log pattern extractor
    assert LogSignalExtractor.extract_error_code("operation failed error_code=ERR_TIMEOUT") == "ERR_TIMEOUT"
    assert LogSignalExtractor.extract_error_code("ok") == "unknown"
