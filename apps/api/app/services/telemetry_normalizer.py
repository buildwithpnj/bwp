class TelemetryNormalizer:
    @classmethod
    def normalize_signal(cls, raw_payload: str) -> str:
        """
        Cleans and normalizes logs/metrics string.
        """
        return raw_payload.strip().lower()
