from typing import Dict, Any, Optional

class RetrievalCacheService:
    _cache: Dict[str, Any] = {}

    @classmethod
    def get_cached_result(cls, query: str, tenant_id: str) -> Optional[Any]:
        """
        Retrieves cached query matches.
        """
        key = f"{tenant_id}:{query}"
        return cls._cache.get(key)

    @classmethod
    def set_cached_result(cls, query: str, tenant_id: str, value: Any) -> None:
        """
        Saves query matches to memory cache.
        """
        key = f"{tenant_id}:{query}"
        cls._cache[key] = value
