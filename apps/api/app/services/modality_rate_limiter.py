import time

class ModalityRateLimiter:
    # Simulates rate limit trackers per tenant
    _requests_history = {}  # tenant_id -> list of timestamps

    @classmethod
    def check_rate_limit(cls, tenant_id: str, max_requests: int = 10, window_sec: int = 60) -> bool:
        """
        Gates excessive ingestion streams by sliding request timestamp windows.
        """
        now = time.time()
        history = cls._requests_history.get(tenant_id, [])
        
        # Filter stale timestamps
        history = [ts for ts in history if now - ts <= window_sec]
        
        if len(history) >= max_requests:
            return False
            
        history.append(now)
        cls._requests_history[tenant_id] = history
        return True
