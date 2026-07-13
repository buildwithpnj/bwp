from app.services.stale_chunk_detector import StaleChunkDetector

def test_stale_chunk_detection():
    assert StaleChunkDetector.is_chunk_stale("h1", "h2") is True
    assert StaleChunkDetector.is_chunk_stale("h1", "h1") is False
