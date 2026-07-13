from app.services.reflection_service import ReflectionService

def test_reflection_critique():
    chunks = [{"chunk_text": "we support active sync configurations"}]
    res = ReflectionService.critique_generation(
        "sync configurations",
        "we support active configurations",
        chunks
    )
    assert res["support_score"] > 0.8
    assert res["should_retry"] is False
