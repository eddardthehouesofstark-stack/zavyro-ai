from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import TicketCategory, TicketPriority, TicketStatus, SlaStatus
from app.schemas.user import UserResponse
from app.schemas.comment import CommentResponse
from app.schemas.attachment import AttachmentResponse
from app.schemas.history import TicketHistoryResponse


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10)
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    device_information: Optional[Dict[str, Any]] = None
    location: Optional[str] = Field(None, max_length=255)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketPriorityUpdate(BaseModel):
    priority: TicketPriority


class TicketAssignUpdate(BaseModel):
    technician_id: Optional[int] = None


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    created_by: int
    assigned_to: Optional[int] = None
    device_information: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_suggested_action: Optional[str] = None
    first_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    response_due_at: Optional[datetime] = None
    resolution_due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    creator: Optional[UserResponse] = None
    assignee: Optional[UserResponse] = None
    sla_status: Optional[SlaStatus] = None

    model_config = ConfigDict(from_attributes=True)


class TicketDetailResponse(TicketResponse):
    comments: List[CommentResponse] = []
    attachments: List[AttachmentResponse] = []
    history: List[TicketHistoryResponse] = []
