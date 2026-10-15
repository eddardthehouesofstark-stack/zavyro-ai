import json
from typing import Any, Optional
import redis
from app.cache.base import CacheBackend
from app.cache.memory import InMemoryCache
from app.core.config import settings
from app.core.logging import logger


class RedisCache(CacheBackend):
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or settings.REDIS_URL
        self._fallback = InMemoryCache()
        try:
            self._client = redis.Redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            # Test ping
            self._client.ping()
            self._available = True
        except Exception as e:
            logger.warning(f"Could not connect to Redis at {self.redis_url}: {e}. Falling back to InMemoryCache.")
            self._client = None
            self._available = False

    def get(self, key: str) -> Optional[Any]:
        if not self._available or not self._client:
            return self._fallback.get(key)
        try:
            raw = self._client.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception as e:
            logger.warning(f"Redis get failed: {e}. Using fallback.")
            return self._fallback.get(key)

    def set(self, key: str, value: Any, ttl_seconds: int = 60) -> None:
        if not self._available or not self._client:
            self._fallback.set(key, value, ttl_seconds)
            return
        try:
            serialized = json.dumps(value)
            if ttl_seconds > 0:
                self._client.setex(key, ttl_seconds, serialized)
            else:
                self._client.set(key, serialized)
        except Exception as e:
            logger.warning(f"Redis set failed: {e}. Using fallback.")
            self._fallback.set(key, value, ttl_seconds)

    def delete(self, key: str) -> bool:
        if not self._available or not self._client:
            return self._fallback.delete(key)
        try:
            return bool(self._client.delete(key))
        except Exception as e:
            logger.warning(f"Redis delete failed: {e}. Using fallback.")
            return self._fallback.delete(key)

    def clear(self) -> None:
        if not self._available or not self._client:
            self._fallback.clear()
            return
        try:
            self._client.flushdb()
        except Exception as e:
            logger.warning(f"Redis clear failed: {e}. Using fallback.")
            self._fallback.clear()
