import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.middleware.preview_rate_limit import PreviewRateLimitMiddleware

client = TestClient(app)

def test_rate_limiting_trigger():
    # Reset limit state
    PreviewRateLimitMiddleware._rate_limits.clear()
    
    # Fire 11 requests (limit is 10)
    responses = []
    for _ in range(12):
        res = client.post("/api/public-preview/session")
        responses.append(res)
        
    status_codes = [r.status_code for r in responses]
    assert 429 in status_codes
