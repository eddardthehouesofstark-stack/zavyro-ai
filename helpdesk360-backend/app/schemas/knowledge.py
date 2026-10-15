from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserResponse


class KnowledgeCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=10)
    category: str = Field(..., min_length=2, max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    content: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    tags: Optional[List[str]] = None


class KnowledgeResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: Optional[List[str]] = []
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    creator: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
