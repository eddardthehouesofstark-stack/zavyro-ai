from functools import lru_cache
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "HelpDesk-360"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./helpdesk360.db"

    JWT_SECRET: str = "helpdesk360-super-secret-jwt-key-for-development-change-in-production-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_TIME: int = 30  # minutes
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    AI_PROVIDER: str = "mock"  # anthropic | openai | mock
    AI_API_KEY: str = ""
    AI_MODEL: str = ""

    FILE_STORAGE_PATH: str = "./uploads"
    STORAGE_BACKEND: str = "local"  # local | s3
    MAX_UPLOAD_MB: int = 10
    ALLOWED_UPLOAD_TYPES: Union[List[str], str] = (
        "image/png,image/jpeg,application/pdf,text/plain,application/zip"
    )

    CORS_ORIGINS: Union[List[str], str] = (
        "http://localhost:3000,http://localhost:5173,http://localhost:5174"
    )

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_BACKEND: str = "memory"  # memory | redis
    RATE_LIMIT_ENABLED: bool = False

    @property
    def allowed_upload_types_list(self) -> List[str]:
        if isinstance(self.ALLOWED_UPLOAD_TYPES, list):
            return self.ALLOWED_UPLOAD_TYPES
        return [x.strip() for x in str(self.ALLOWED_UPLOAD_TYPES).split(",") if x.strip()]

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [x.strip() for x in str(self.CORS_ORIGINS).split(",") if x.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
