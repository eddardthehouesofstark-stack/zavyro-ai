from abc import ABC, abstractmethod
from typing import BinaryIO, Tuple


class StorageBackend(ABC):
    @abstractmethod
    def save(self, file_content: bytes, original_filename: str, content_type: str) -> Tuple[str, str]:
        """
        Saves file content and returns (stored_filename_or_key, public_or_relative_url)
        """
        pass

    @abstractmethod
    def get(self, file_key: str) -> bytes:
        """
        Retrieves file bytes by key/path
        """
        pass

    @abstractmethod
    def delete(self, file_key: str) -> bool:
        """
        Deletes file by key/path
        """
        pass
