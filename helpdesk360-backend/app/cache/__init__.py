from functools import lru_cache
from app.core.config import settings
from app.cache.base import CacheBackend
from app.cache.memory import InMemoryCache
from app.cache.redis import RedisCache


@lru_cache()
def get_cache() -> CacheBackend:
    if settings.CACHE_BACKEND.lower() == "redis":
        return RedisCache()
    return InMemoryCache()


__all__ = ["CacheBackend", "InMemoryCache", "RedisCache", "get_cache"]
