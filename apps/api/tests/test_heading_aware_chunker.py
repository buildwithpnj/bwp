import pytest
from app.services.heading_aware_chunker import HeadingAwareChunker
from app.services.chunk_quality_service import ChunkQualityService
from app.services.semantic_overlap_service import SemanticOverlapService

def test_structural_chunking():
    # 1. Split text parameters by headers
    raw = "# Section A\nThis is paragraph A\n## Section B\nThis is paragraph B"
    chunks = HeadingAwareChunker.split_by_headings(raw)
    assert len(chunks) == 2
    assert chunks[0]["heading"] == "Section A"
    assert chunks[1]["heading"] == "Section B"
    
    # 2. Quality validation gates
    assert ChunkQualityService.validate_chunk("short") is False
    assert ChunkQualityService.validate_chunk("this is a valid long text parameter") is True
    
    # 3. Overlap context injection
    overlapped = SemanticOverlapService.attach_context_buffer([
        {"heading": "A", "text": "This is sample body text A"},
        {"heading": "B", "text": "This is sample body text B"}
    ])
    assert "A" in overlapped[1]["text"]
