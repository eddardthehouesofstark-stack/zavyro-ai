from enum import Enum


class RoleEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    TECHNICIAN = "TECHNICIAN"


class TicketCategory(str, Enum):
    HARDWARE = "HARDWARE"
    SOFTWARE = "SOFTWARE"
    NETWORK = "NETWORK"
    ACCESS = "ACCESS"
    EMAIL = "EMAIL"
    SECURITY = "SECURITY"
    OTHER = "OTHER"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketStatus(str, Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_EMPLOYEE = "WAITING_FOR_EMPLOYEE"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class CommentType(str, Enum):
    EMPLOYEE_REPLY = "EMPLOYEE_REPLY"
    TECHNICIAN_REPLY = "TECHNICIAN_REPLY"
    INTERNAL_NOTE = "INTERNAL_NOTE"


class NotificationType(str, Enum):
    TICKET_CREATED = "TICKET_CREATED"
    TICKET_ASSIGNED = "TICKET_ASSIGNED"
    STATUS_CHANGED = "STATUS_CHANGED"
    NEW_COMMENT = "NEW_COMMENT"
    SLA_WARNING = "SLA_WARNING"
    SLA_BREACH = "SLA_BREACH"


class SlaStatus(str, Enum):
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    BREACHED = "BREACHED"
    MET = "MET"
