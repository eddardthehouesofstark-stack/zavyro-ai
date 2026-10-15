import uuid
from typing import Tuple
from app.storage.base import StorageBackend
from app.core.exceptions import AppException


class S3Storage(StorageBackend):
    def __init__(self, bucket_name: str = "helpdesk360-bucket", region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region_name = region_name

    def save(self, file_content: bytes, original_filename: str, content_type: str) -> Tuple[str, str]:
        unique_key = f"uploads/{uuid.uuid4().hex}_{original_filename}"
        # Stub: when boto3 client is configured:
        # s3_client.put_object(Bucket=self.bucket_name, Key=unique_key, Body=file_content, ContentType=content_type)
        url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{unique_key}"
        return unique_key, url

    def get(self, file_key: str) -> bytes:
        # Stub:
        # response = s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
        # return response['Body'].read()
        return b""

    def delete(self, file_key: str) -> bool:
        # Stub:
        # s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
        return True
