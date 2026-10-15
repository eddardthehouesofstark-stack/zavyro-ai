from sqlalchemy import Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.enums import TicketPriority


class SlaRule(Base):
    __tablename__ = "sla_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    priority: Mapped[TicketPriority] = mapped_column(
        SAEnum(TicketPriority, name="sla_priority"),
        unique=True,
        nullable=False,
    )
    response_time: Mapped[int] = mapped_column(Integer, nullable=False)  # minutes
    resolution_time: Mapped[int] = mapped_column(Integer, nullable=False)  # minutes
