import pytest
from app.services.context_compression_service import ContextCompressionService
from app.services.evidence_pack_builder import EvidencePackBuilder

def test_context_compression_limits():
    # 1. Assembling evidence packs
    chunks = [
        {"chunk_id": "c1", "chunk_text": "This is chunk text one", "chunk_summary": "Summary A"},
        {"chunk_id": "c2", "chunk_text": "This is chunk text two", "chunk_summary": "Summary B"}
    ]
    pack = EvidencePackBuilder.assemble_pack("sample query", chunks)
    assert len(pack["evidence_blocks"]) == 2
    
    # 2. Compressing under token budget limits
    compressed = ContextCompressionService.compress_pack(pack, token_limit=5)
    # The first chunk text has 5 words, so it should fit exactly. The second should be truncated.
    assert len(compressed["evidence_blocks"]) == 1
