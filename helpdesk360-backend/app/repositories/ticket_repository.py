from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func, and_, or_, desc, asc
from app.models.ticket import Ticket
from app.models.enums import TicketCategory, TicketPriority, TicketStatus
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: Session):
        super().__init__(Ticket, db)

    def get_with_details(self, ticket_id: int) -> Optional[Ticket]:
        stmt = (
            select(Ticket)
            .where(Ticket.id == ticket_id)
            .options(
                selectinload(Ticket.creator),
                selectinload(Ticket.assignee),
                selectinload(Ticket.comments),
                selectinload(Ticket.attachments),
                selectinload(Ticket.history),
            )
        )
        return self.db.scalars(stmt).first()

    def get_by_number(self, ticket_number: str) -> Optional[Ticket]:
        stmt = (
            select(Ticket)
            .where(Ticket.ticket_number == ticket_number)
            .options(
                selectinload(Ticket.creator),
                selectinload(Ticket.assignee),
            )
        )
        return self.db.scalars(stmt).first()

    def get_next_sequence_id(self) -> int:
        stmt = select(func.coalesce(func.max(Ticket.id), 0) + 1)
        res = self.db.scalar(stmt)
        return res or 1

    def list_my_tickets(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TicketStatus] = None,
        priority: Optional[TicketPriority] = None,
        category: Optional[TicketCategory] = None,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ) -> Tuple[List[Ticket], int]:
        stmt = (
            select(Ticket)
            .where(Ticket.created_by == user_id)
            .options(
                selectinload(Ticket.creator),
                selectinload(Ticket.assignee),
            )
        )
        count_stmt = select(func.count(Ticket.id)).where(Ticket.created_by == user_id)

        if status:
            stmt = stmt.where(Ticket.status == status)
            count_stmt = count_stmt.where(Ticket.status == status)
        if priority:
            stmt = stmt.where(Ticket.priority == priority)
            count_stmt = count_stmt.where(Ticket.priority == priority)
        if category:
            stmt = stmt.where(Ticket.category == category)
            count_stmt = count_stmt.where(Ticket.category == category)

        # Sorting
        order_col = getattr(Ticket, sort_by) if sort_by and hasattr(Ticket, sort_by) else Ticket.created_at
        stmt = stmt.order_by(desc(order_col) if order == "desc" else asc(order_col))

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset(skip).limit(limit)).all())
        return items, total

    def list_technician_tickets(
        self,
        technician_id: int,
        unassigned: bool = False,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TicketStatus] = None,
        priority: Optional[TicketPriority] = None,
        category: Optional[TicketCategory] = None,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ) -> Tuple[List[Ticket], int]:
        stmt = select(Ticket).options(
            selectinload(Ticket.creator),
            selectinload(Ticket.assignee),
        )
        count_stmt = select(func.count(Ticket.id))

        if unassigned:
            condition = Ticket.assigned_to.is_(None)
        else:
            condition = or_(Ticket.assigned_to == technician_id, Ticket.assigned_to.is_(None))

        stmt = stmt.where(condition)
        count_stmt = count_stmt.where(condition)

        if status:
            stmt = stmt.where(Ticket.status == status)
            count_stmt = count_stmt.where(Ticket.status == status)
        if priority:
            stmt = stmt.where(Ticket.priority == priority)
            count_stmt = count_stmt.where(Ticket.priority == priority)
        if category:
            stmt = stmt.where(Ticket.category == category)
            count_stmt = count_stmt.where(Ticket.category == category)

        order_col = getattr(Ticket, sort_by) if sort_by and hasattr(Ticket, sort_by) else Ticket.created_at
        stmt = stmt.order_by(desc(order_col) if order == "desc" else asc(order_col))

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset(skip).limit(limit)).all())
        return items, total

    def list_all_filtered(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TicketStatus] = None,
        priority: Optional[TicketPriority] = None,
        category: Optional[TicketCategory] = None,
        assigned_to: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ) -> Tuple[List[Ticket], int]:
        stmt = select(Ticket).options(
            selectinload(Ticket.creator),
            selectinload(Ticket.assignee),
        )
        count_stmt = select(func.count(Ticket.id))

        conditions = []
        if status:
            conditions.append(Ticket.status == status)
        if priority:
            conditions.append(Ticket.priority == priority)
        if category:
            conditions.append(Ticket.category == category)
        if assigned_to is not None:
            conditions.append(Ticket.assigned_to == assigned_to)
        if date_from:
            conditions.append(Ticket.created_at >= date_from)
        if date_to:
            conditions.append(Ticket.created_at <= date_to)

        if conditions:
            stmt = stmt.where(and_(*conditions))
            count_stmt = count_stmt.where(and_(*conditions))

        order_col = getattr(Ticket, sort_by) if sort_by and hasattr(Ticket, sort_by) else Ticket.created_at
        stmt = stmt.order_by(desc(order_col) if order == "desc" else asc(order_col))

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset(skip).limit(limit)).all())
        return items, total

    def get_open_tickets(self) -> List[Ticket]:
        open_statuses = [
            TicketStatus.NEW,
            TicketStatus.ASSIGNED,
            TicketStatus.IN_PROGRESS,
            TicketStatus.WAITING_FOR_EMPLOYEE,
        ]
        stmt = select(Ticket).where(Ticket.status.in_(open_statuses))
        return list(self.db.scalars(stmt).all())
