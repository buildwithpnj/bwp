from app.services.vector_store_service import VectorStoreService

def test_cosine_similarity_accuracy():
    vec_a = [1.0, 0.0]
    vec_b = [1.0, 0.0]
    cands = [{"vector": vec_b, "chunk_id": "c1"}]
    results = VectorStoreService.search_similar_vectors(vec_a, cands)
    assert len(results) == 1
    assert results[0]["score"] > 0.99
