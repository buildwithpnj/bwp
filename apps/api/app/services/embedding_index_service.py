from typing import List

class EmbeddingIndexService:
    @classmethod
    def generate_mock_embedding(cls, text: str) -> List[float]:
        """
        Creates floating-point model embeddings array from query string.
        """
        val = sum(ord(c) for c in text) % 100 / 100.0
        # Return a simple mock vector
        return [val] * 8
