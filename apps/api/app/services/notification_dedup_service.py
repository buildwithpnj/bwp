import time

class NotificationDedupService:
    # In-memory deduplication cache: (user_id, title) -> timestamp
    _last_sent = {}

    @classmethod
    def is_duplicate(cls, user_id: str, title: str, cooldown_seconds: int = 60) -> bool:
        """
        Deduplicates identical notification alerts within a brief sliding window.
        """
        key = (user_id, title)
        now = time.time()
        last = cls._last_sent.get(key, 0.0)
        
        if now - last <= cooldown_seconds:
            return True
            
        cls._last_sent[key] = now
        return False
