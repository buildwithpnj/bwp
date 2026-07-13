from typing import List, Dict, Any

class IndexIntegrityChecker:
    @classmethod
    def verify_integrity(cls, documents: List[Dict[str, Any]], chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates index structures, identifying orphaned chunks.
        """
        doc_ids = {d["id"] for d in documents}
        orphaned = []
        for c in chunks:
            if c["document_id"] not in doc_ids:
                orphaned.append(c["id"])
                
        return {
            "healthy": len(orphaned) == 0,
            "orphaned_chunks_count": len(orphaned),
            "orphaned_chunk_ids": orphaned
        }
