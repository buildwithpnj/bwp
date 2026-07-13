from app.services.index_integrity_checker import IndexIntegrityChecker

def test_index_integrity():
    docs = [{"id": "d1"}]
    chunks = [{"id": "c1", "document_id": "d1"}]
    res = IndexIntegrityChecker.verify_integrity(docs, chunks)
    assert res["healthy"] is True
