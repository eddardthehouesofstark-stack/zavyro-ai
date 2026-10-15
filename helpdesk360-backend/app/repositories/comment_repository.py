from typing import List
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.comment import TicketComment
from app.models.enums import CommentType
from app.repositories.base import BaseRepository


class CommentRepository(BaseRepository[TicketComment]):
    def __init__(self, db: Session):
        super().__init__(TicketComment, db)

    def list_by_ticket(self, ticket_id: int, include_internal: bool = False) -> List[TicketComment]:
        stmt = (
            select(TicketComment)
            .where(TicketComment.ticket_id == ticket_id)
            .options(selectinload(TicketComment.user))
            .order_by(TicketComment.created_at.asc())
        )
        if not include_internal:
            stmt = stmt.where(TicketComment.comment_type != CommentType.INTERNAL_NOTE)
        return list(self.db.scalars(stmt).all())
