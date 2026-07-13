class IngestCostEstimator:
    @classmethod
    def estimate_processing_tokens(cls, media_type: str, file_size_bytes: int) -> float:
        """
        Estimates the processing token cost weight based on file modality types.
        """
        # PDFs are heavy
        if media_type in ["pdf", "document"]:
            return 2.5 + (file_size_bytes / 1024 / 1024) * 0.5
        # Screenshots are medium
        if media_type in ["screenshot", "image"]:
            return 1.5
        return 1.0
