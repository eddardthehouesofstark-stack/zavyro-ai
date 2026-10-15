import os
import uuid
from typing import Tuple
from app.core.config import settings
from app.core.exceptions import BadRequestException, NotFoundException
from app.storage.base import StorageBackend


class LocalStorage(StorageBackend):
    def __init__(self, base_path: str = None):
        self.base_path = os.path.abspath(base_path or settings.FILE_STORAGE_PATH)
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, file_content: bytes, original_filename: str, content_type: str) -> Tuple[str, str]:
        ext = os.path.splitext(original_filename)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        target_path = os.path.join(self.base_path, unique_name)

        with open(target_path, "wb") as f:
            f.write(file_content)

        file_url = f"/api/v1/tickets/attachments/download/{unique_name}"
        return unique_name, file_url

    def get(self, file_key: str) -> bytes:
        # Prevent path traversal
        clean_key = os.path.basename(file_key)
        target_path = os.path.join(self.base_path, clean_key)

        if not os.path.exists(target_path):
            raise NotFoundException(f"Attachment {clean_key} not found")

        with open(target_path, "rb") as f:
            return f.read()

    def delete(self, file_key: str) -> bool:
        clean_key = os.path.basename(file_key)
        target_path = os.path.join(self.base_path, clean_key)
        if os.path.exists(target_path):
            os.remove(target_path)
            return True
        return False
