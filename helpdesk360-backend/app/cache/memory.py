import time
from typing import Any, Dict, Optional, Tuple
from app.cache.base import CacheBackend


class InMemoryCache(CacheBackend):
    def __init__(self):
        # key -> (value, expire_timestamp)
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        val, expires_at = self._store[key]
        if expires_at is not None and time.time() > expires_at:
            del self._store[key]
            return None
        return val

    def set(self, key: str, value: Any, ttl_seconds: int = 60) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds > 0 else None
        self._store[key] = (value, expires_at)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        self._store.clear()
