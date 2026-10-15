from typing import List
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.history import TicketHistory
from app.repositories.base import BaseRepository


class HistoryRepository(BaseRepository[TicketHistory]):
    def __init__(self, db: Session):
        super().__init__(TicketHistory, db)

    def list_by_ticket(self, ticket_id: int) -> List[TicketHistory]:
        stmt = (
            select(TicketHistory)
            .where(TicketHistory.ticket_id == ticket_id)
            .options(selectinload(TicketHistory.user))
            .order_by(TicketHistory.timestamp.asc())
        )
        return list(self.db.scalars(stmt).all())
