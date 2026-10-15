from functools import lru_cache
from app.core.config import settings
from app.storage.base import StorageBackend
from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage


@lru_cache()
def get_storage() -> StorageBackend:
    if settings.STORAGE_BACKEND.lower() == "s3":
        return S3Storage()
    return LocalStorage()


__all__ = ["StorageBackend", "LocalStorage", "S3Storage", "get_storage"]
