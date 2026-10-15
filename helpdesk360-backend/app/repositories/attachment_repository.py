from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.attachment import Attachment
from app.repositories.base import BaseRepository


class AttachmentRepository(BaseRepository[Attachment]):
    def __init__(self, db: Session):
        super().__init__(Attachment, db)

    def get_by_id(self, attachment_id: int) -> Optional[Attachment]:
        stmt = (
            select(Attachment)
            .where(Attachment.id == attachment_id)
            .options(selectinload(Attachment.uploader))
        )
        return self.db.scalars(stmt).first()

    def list_by_ticket(self, ticket_id: int) -> List[Attachment]:
        stmt = (
            select(Attachment)
            .where(Attachment.ticket_id == ticket_id)
            .options(selectinload(Attachment.uploader))
            .order_by(Attachment.created_at.asc())
        )
        return list(self.db.scalars(stmt).all())
