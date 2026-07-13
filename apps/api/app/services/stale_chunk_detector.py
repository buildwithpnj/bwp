class StaleChunkDetector:
    @classmethod
    def is_chunk_stale(cls, document_hash: str, index_hash: str) -> bool:
        """
        Detects if indexed chunk details are outdated compared to document content hashes.
        """
        if not document_hash or not index_hash:
            return True
        return document_hash != index_hash
