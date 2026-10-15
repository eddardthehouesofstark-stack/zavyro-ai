from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import TicketPriority, SlaStatus


class SlaRuleResponse(BaseModel):
    id: int
    priority: TicketPriority
    response_time: int  # minutes
    resolution_time: int  # minutes

    model_config = ConfigDict(from_attributes=True)


class SlaRuleUpdate(BaseModel):
    response_time: int = Field(..., ge=1)
    resolution_time: int = Field(..., ge=1)


class TicketSlaResponse(BaseModel):
    ticket_id: int
    ticket_number: str
    priority: TicketPriority
    response_due_at: Optional[datetime] = None
    resolution_due_at: Optional[datetime] = None
    first_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    response_status: SlaStatus
    resolution_status: SlaStatus
    overall_status: SlaStatus


class SlaSummaryResponse(BaseModel):
    total_open: int
    on_track: int
    at_risk: int
    breached: int
    met: int
