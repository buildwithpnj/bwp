from app.services.embedding_retrieval_service import EmbeddingRetrievalService

def test_fetch_similar_chunks():
    candidates = [
        {"chunk_id": "c1", "document_id": "d1", "chunk_text": "sample target chunk text", "chunk_summary": "summary text"}
    ]
    results = EmbeddingRetrievalService.fetch_similar_chunks("sample query", candidates)
    assert len(results) == 1
    assert "score" in results[0]
