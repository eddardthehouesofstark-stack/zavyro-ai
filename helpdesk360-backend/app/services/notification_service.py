from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.enums import NotificationType, RoleEnum
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.websocket.manager import ws_manager
from app.core.logging import logger


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NotificationRepository(db)
        self.user_repo = UserRepository(db)

    async def create_and_send(
        self,
        user_id: int,
        title: str,
        message: str,
        type: NotificationType,
        ticket_id: Optional[int] = None,
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            ticket_id=ticket_id,
            is_read=False,
        )
        saved = self.repo.create(notif)

        # Push real-time WebSocket update
        try:
            payload = {
                "id": saved.id,
                "user_id": saved.user_id,
                "title": saved.title,
                "message": saved.message,
                "type": saved.type.value if hasattr(saved.type, "value") else str(saved.type),
                "ticket_id": saved.ticket_id,
                "is_read": saved.is_read,
                "created_at": saved.created_at.isoformat() if saved.created_at else None,
            }
            await ws_manager.send_to_user(user_id, "NOTIFICATION", payload)
        except Exception as e:
            logger.warning(f"Failed to push notification over WebSocket to user {user_id}: {e}")

        return saved

    async def notify_technicians(
        self,
        title: str,
        message: str,
        type: NotificationType,
        ticket_id: Optional[int] = None,
    ) -> List[Notification]:
        technicians = self.user_repo.list_technicians()
        results = []
        for tech in technicians:
            notif = await self.create_and_send(
                user_id=tech.id,
                title=title,
                message=message,
                type=type,
                ticket_id=ticket_id,
            )
            results.append(notif)
        return results

    def list_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Notification], int]:
        return self.repo.list_by_user(user_id=user_id, unread_only=unread_only, skip=skip, limit=limit)

    def get_unread_count(self, user_id: int) -> int:
        return self.repo.count_unread(user_id)

    def mark_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        return self.repo.mark_as_read(notification_id, user_id)

    def mark_all_read(self, user_id: int) -> int:
        return self.repo.mark_all_read(user_id)
