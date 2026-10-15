from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, update
from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(Notification, db)

    def list_by_user(
        self,
        user_id: int,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Notification], int]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        count_stmt = select(func.count(Notification.id)).where(Notification.user_id == user_id)

        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
            count_stmt = count_stmt.where(Notification.is_read == False)

        stmt = stmt.order_by(desc(Notification.created_at))
        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset(skip).limit(limit)).all())
        return items, total

    def count_unread(self, user_id: int) -> int:
        stmt = select(func.count(Notification.id)).where(
            Notification.user_id == user_id,
            Notification.is_read == False,
        )
        return self.db.scalar(stmt) or 0

    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        notif = self.get_by_id(notification_id)
        if notif and notif.user_id == user_id:
            notif.is_read = True
            self.db.commit()
            self.db.refresh(notif)
            return notif
        return None

    def mark_all_read(self, user_id: int) -> int:
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .values(is_read=True)
        )
        res = self.db.execute(stmt)
        self.db.commit()
        return res.rowcount
