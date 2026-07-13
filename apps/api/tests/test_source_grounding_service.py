from app.services.source_grounding_service import SourceGroundingService

def test_ground_response():
    chunks = [
        {"chunk_id": "c1", "document_id": "d1", "chunk_summary": "policy configuration sync matches"}
    ]
    res = SourceGroundingService.ground_response("sync parameters look matches", chunks)
    assert res["grounded"] is True
    assert len(res["citations"]) == 1
