from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.sla import SlaRule
from app.models.enums import TicketPriority
from app.repositories.base import BaseRepository


class SlaRepository(BaseRepository[SlaRule]):
    def __init__(self, db: Session):
        super().__init__(SlaRule, db)

    def get_by_priority(self, priority: TicketPriority) -> Optional[SlaRule]:
        stmt = select(SlaRule).where(SlaRule.priority == priority)
        return self.db.scalars(stmt).first()

    def list_rules(self) -> List[SlaRule]:
        stmt = select(SlaRule).order_by(SlaRule.id.asc())
        return list(self.db.scalars(stmt).all())

    def update_rule(self, priority: TicketPriority, response_time: int, resolution_time: int) -> Optional[SlaRule]:
        rule = self.get_by_priority(priority)
        if not rule:
            rule = SlaRule(
                priority=priority,
                response_time=response_time,
                resolution_time=resolution_time,
            )
            self.db.add(rule)
        else:
            rule.response_time = response_time
            rule.resolution_time = resolution_time
        self.db.commit()
        self.db.refresh(rule)
        return rule
