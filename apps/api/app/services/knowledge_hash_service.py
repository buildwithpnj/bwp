import hashlib

class KnowledgeHashService:
    @classmethod
    def compute_hash(cls, text: str) -> str:
        """
        Computes SHA256 checksum of document string content.
        """
        if not text:
            return ""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
