from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func, or_, desc
from app.models.knowledge import KnowledgeArticle
from app.repositories.base import BaseRepository


class KnowledgeRepository(BaseRepository[KnowledgeArticle]):
    def __init__(self, db: Session):
        super().__init__(KnowledgeArticle, db)

    def get_by_id(self, article_id: int) -> Optional[KnowledgeArticle]:
        stmt = (
            select(KnowledgeArticle)
            .where(KnowledgeArticle.id == article_id)
            .options(selectinload(KnowledgeArticle.creator))
        )
        return self.db.scalars(stmt).first()

    def list_articles(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Tuple[List[KnowledgeArticle], int]:
        stmt = select(KnowledgeArticle).options(selectinload(KnowledgeArticle.creator))
        count_stmt = select(func.count(KnowledgeArticle.id))

        if category:
            stmt = stmt.where(KnowledgeArticle.category.ilike(category))
            count_stmt = count_stmt.where(KnowledgeArticle.category.ilike(category))

        # Sort newest first
        stmt = stmt.order_by(desc(KnowledgeArticle.created_at))

        # Tag filtering in memory or query if needed
        all_articles = list(self.db.scalars(stmt).all())
        if tag:
            all_articles = [a for a in all_articles if a.tags and tag.lower() in [t.lower() for t in a.tags]]

        total = len(all_articles)
        items = all_articles[skip : skip + limit]
        return items, total

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> Tuple[List[KnowledgeArticle], int]:
        q = f"%{query.strip()}%"
        stmt = select(KnowledgeArticle).options(selectinload(KnowledgeArticle.creator)).where(
            or_(
                KnowledgeArticle.title.ilike(q),
                KnowledgeArticle.content.ilike(q),
                KnowledgeArticle.category.ilike(q),
            )
        )
        count_stmt = select(func.count(KnowledgeArticle.id)).where(
            or_(
                KnowledgeArticle.title.ilike(q),
                KnowledgeArticle.content.ilike(q),
                KnowledgeArticle.category.ilike(q),
            )
        )
        if category:
            stmt = stmt.where(KnowledgeArticle.category.ilike(category))
            count_stmt = count_stmt.where(KnowledgeArticle.category.ilike(category))

        stmt = stmt.order_by(desc(KnowledgeArticle.updated_at))
        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset(skip).limit(limit)).all())
        return items, total
