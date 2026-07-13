class MultimodalSummaryCompactor:
    @classmethod
    def compact_multimodal_extraction(cls, text: str) -> str:
        """
        Compresses raw document extractions to save prompt space.
        """
        if len(text) < 100:
            return text
        return text[:100] + "... [Truncated for prompt efficiency]"
