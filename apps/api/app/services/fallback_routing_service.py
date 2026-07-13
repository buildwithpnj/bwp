class FallbackRoutingService:
    @classmethod
    def get_fallback_provider(cls, primary_provider: str, degradation_level: str) -> str:
        """
        Calculates cheaper fallback model/provider paths during traffic/latency spikes.
        """
        if degradation_level == "critical":
            return "ollama_local"
        elif degradation_level == "degraded":
            return "gpt-4o-mini"
        return primary_provider
