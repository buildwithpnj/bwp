from typing import Dict, Any, Optional

class EvidenceCacheService:
    _cache: Dict[str, Any] = {}

    @classmethod
    def get_cached_pack(cls, query: str, tenant_id: str) -> Optional[Any]:
        """
        Retrieves cached evidence block packs.
        """
        key = f"{tenant_id}:{query}"
        return cls._cache.get(key)

    @classmethod
    def set_cached_pack(cls, query: str, tenant_id: str, value: Any) -> None:
        """
        Saves evidence block packs to cache mapping.
        """
        key = f"{tenant_id}:{query}"
        cls._cache[key] = value
