from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse


class AttachmentResponse(BaseModel):
    id: int
    ticket_id: int
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_by: Optional[int] = None
    created_at: datetime
    uploader: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
