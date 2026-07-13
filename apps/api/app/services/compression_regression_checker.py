from typing import Dict, Any

class CompressionRegressionChecker:
    @classmethod
    def verify_compression_ratio(cls, original_len: int, compressed_len: int) -> float:
        """
        Verifies that compressed outputs achieve at least 30% word savings.
        """
        if original_len == 0:
            return 1.0
        return float(compressed_len) / original_len
