from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse


class TicketHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    action: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    changed_by: Optional[int] = None
    timestamp: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
