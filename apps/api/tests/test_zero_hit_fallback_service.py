from app.services.zero_hit_fallback_service import ZeroHitFallbackService

def test_zero_hit_fallback():
    suggestions = ZeroHitFallbackService.get_fallback_suggestions("policy missing keys")
    assert len(suggestions) > 0
    assert "policy sync" in suggestions
