from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.enums import TicketCategory, TicketPriority


class AiAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5)


class AiAnalysisResult(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    summary: str
    suggested_action: str


class AiSummarizeResponse(BaseModel):
    ticket_id: int
    summary: str


class AiTroubleshootResponse(BaseModel):
    ticket_id: int
    steps: List[str]


class AiDraftReplyResponse(BaseModel):
    ticket_id: int
    draft_reply: str


class AiArticleReference(BaseModel):
    id: int
    title: str


class AiResolutionResponse(BaseModel):
    ticket_id: int
    summary: str
    solution: str
    steps: List[str] = []
    articles: List[AiArticleReference] = []


class TicketDraft(BaseModel):
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority


class AiChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None


class AiChatResponse(BaseModel):
    reply: str
    suggest_ticket: bool = False
    ticket_draft: Optional[TicketDraft] = None
    conversation_id: Optional[str] = None


class AiAssistResponse(BaseModel):
    summary: str
    solution: str
    draftReply: str
    steps: List[str]
    articles: List[Dict[str, Any]]
