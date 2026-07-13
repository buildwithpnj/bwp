from app.services.retrieval_candidate_merger import RetrievalCandidateMerger

def test_merge_candidates():
    lexical = [{"chunk_id": "c1", "document_id": "d1", "chunk_text": "text", "chunk_summary": "sum", "score": 0.7}]
    vector = [{"chunk_id": "c1", "document_id": "d1", "chunk_text": "text", "chunk_summary": "sum", "score": 0.9}]
    merged = RetrievalCandidateMerger.merge_candidates(lexical, vector)
    assert len(merged) == 1
    assert merged[0]["score"] == 0.9
