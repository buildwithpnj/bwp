class RetrievalCostEstimator:
    @classmethod
    def estimate_savings(cls, original_word_count: int, compressed_word_count: int) -> float:
        """
        Estimates dollar savings achieved by context compression algorithms.
        """
        saved = max(0, original_word_count - compressed_word_count)
        # Assume $0.00001 per word cost
        return saved * 0.00001
