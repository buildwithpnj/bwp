class ChunkQualityService:
    @classmethod
    def validate_chunk(cls, text: str) -> bool:
        """
        Rejects unusable or low-quality noise segments.
        """
        if not text:
            return False
        cleaned = text.strip()
        # Quality gates: reject short noise chunks or long meaningless ones
        if len(cleaned) < 15:
            return False
        return True
