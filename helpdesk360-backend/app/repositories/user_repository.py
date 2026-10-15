from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.user import User
from app.models.enums import RoleEnum
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email.lower().strip())
        return self.db.scalars(stmt).first()

    def list_technicians(self) -> List[User]:
        stmt = select(User).where(User.role == RoleEnum.TECHNICIAN, User.is_active == True)
        return list(self.db.scalars(stmt).all())

    def list_users(
        self,
        skip: int = 0,
        limit: int = 10,
        role: Optional[RoleEnum] = None,
        department: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> List[User]:
        stmt = select(User)
        if role is not None:
            stmt = stmt.where(User.role == role)
        if department:
            stmt = stmt.where(User.department.ilike(f"%{department}%"))
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where((User.name.ilike(pattern)) | (User.email.ilike(pattern)))
        stmt = stmt.order_by(User.id.asc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count_users(
        self,
        role: Optional[RoleEnum] = None,
        department: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        stmt = select(func.count(User.id))
        if role is not None:
            stmt = stmt.where(User.role == role)
        if department:
            stmt = stmt.where(User.department.ilike(f"%{department}%"))
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where((User.name.ilike(pattern)) | (User.email.ilike(pattern)))
        return self.db.scalar(stmt) or 0
