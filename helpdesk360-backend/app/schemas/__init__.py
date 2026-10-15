from app.schemas.user import UserBase, UserResponse, UserUpdate
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.schemas.ticket import (
    TicketCreate,
    TicketStatusUpdate,
    TicketPriorityUpdate,
    TicketAssignUpdate,
    TicketResponse,
    TicketDetailResponse,
)
from app.schemas.comment import CommentCreate, CommentResponse
from app.schemas.attachment import AttachmentResponse
from app.schemas.history import TicketHistoryResponse
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate, KnowledgeResponse
from app.schemas.notification import NotificationResponse, UnreadCountResponse
from app.schemas.sla import SlaRuleResponse, SlaRuleUpdate, TicketSlaResponse, SlaSummaryResponse
from app.schemas.analytics import AnalyticsDashboardResponse, AnalyticsTotals
from app.schemas.search import SearchResponse, SearchResultItem
from app.schemas.ai import (
    AiAnalyzeRequest,
    AiAnalysisResult,
    AiSummarizeResponse,
    AiTroubleshootResponse,
    AiDraftReplyResponse,
    AiResolutionResponse,
    AiChatRequest,
    AiChatResponse,
    AiAssistResponse,
    TicketDraft,
)

__all__ = [
    "UserBase",
    "UserResponse",
    "UserUpdate",
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "TicketCreate",
    "TicketStatusUpdate",
    "TicketPriorityUpdate",
    "TicketAssignUpdate",
    "TicketResponse",
    "TicketDetailResponse",
    "CommentCreate",
    "CommentResponse",
    "AttachmentResponse",
    "TicketHistoryResponse",
    "KnowledgeCreate",
    "KnowledgeUpdate",
    "KnowledgeResponse",
    "NotificationResponse",
    "UnreadCountResponse",
    "SlaRuleResponse",
    "SlaRuleUpdate",
    "TicketSlaResponse",
    "SlaSummaryResponse",
    "AnalyticsDashboardResponse",
    "AnalyticsTotals",
    "SearchResponse",
    "SearchResultItem",
    "AiAnalyzeRequest",
    "AiAnalysisResult",
    "AiSummarizeResponse",
    "AiTroubleshootResponse",
    "AiDraftReplyResponse",
    "AiResolutionResponse",
    "AiChatRequest",
    "AiChatResponse",
    "AiAssistResponse",
    "TicketDraft",
]
