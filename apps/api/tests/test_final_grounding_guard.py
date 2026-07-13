import pytest
from app.services.final_grounding_guard import FinalGroundingGuard

def test_final_grounding_guard_success():
    answer = "git sync configuration rules"
    evidence_chunks = [
        {"chunk_id": "c1", "document_id": "doc_1", "chunk_summary": "git sync configuration rules"}
    ]
    
    result = FinalGroundingGuard.validate_and_gate_response(
        answer=answer,
        evidence_chunks=evidence_chunks,
        base_confidence=0.85
    )
    
    assert result["grounded"] is True
    assert result["confidence"] > 0.7
    assert len(result["citations"]) == 1

def test_final_grounding_guard_blocked_claims():
    answer = "The system is fully synchronized with Azure credentials."
    evidence_chunks = [
        {"chunk_id": "c1", "document_id": "doc_1", "chunk_summary": "only database schema backups exist"}
    ]
    
    result = FinalGroundingGuard.validate_and_gate_response(
        answer=answer,
        evidence_chunks=evidence_chunks,
        base_confidence=0.8
    )
    
    assert result["grounded"] is False
    assert "Abstaining from answering" in result["answer"]
    assert result["confidence"] == 0.0
