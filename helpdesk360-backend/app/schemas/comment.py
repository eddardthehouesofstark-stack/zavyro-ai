from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import CommentType
from app.schemas.user import UserResponse


class CommentCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    comment_type: CommentType = CommentType.EMPLOYEE_REPLY


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    comment_type: CommentType
    created_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
