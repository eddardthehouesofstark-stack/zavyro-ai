from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List, Dict
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.sla import SlaRule
from app.models.enums import TicketPriority, TicketStatus, SlaStatus, NotificationType
from app.repositories.sla_repository import SlaRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.sla import TicketSlaResponse, SlaSummaryResponse
from app.core.logging import logger

# Default SLA times in minutes
DEFAULT_SLA_CONFIG = {
    TicketPriority.CRITICAL: {"response_time": 15, "resolution_time": 240},
    TicketPriority.HIGH: {"response_time": 60, "resolution_time": 480},
    TicketPriority.MEDIUM: {"response_time": 240, "resolution_time": 1440},
    TicketPriority.LOW: {"response_time": 480, "resolution_time": 4320},
}


class SlaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SlaRepository(db)
        self.ticket_repo = TicketRepository(db)

    def get_rule_for_priority(self, priority: TicketPriority) -> Dict[str, int]:
        rule = self.repo.get_by_priority(priority)
        if rule:
            return {"response_time": rule.response_time, "resolution_time": rule.resolution_time}
        return DEFAULT_SLA_CONFIG.get(priority, {"response_time": 240, "resolution_time": 1440})

    def compute_due_dates(
        self,
        priority: TicketPriority,
        start_time: Optional[datetime] = None,
    ) -> Tuple[datetime, datetime]:
        base_time = start_time or datetime.now(timezone.utc)
        rule = self.get_rule_for_priority(priority)
        response_due = base_time + timedelta(minutes=rule["response_time"])
        resolution_due = base_time + timedelta(minutes=rule["resolution_time"])
        return response_due, resolution_due

    def calculate_ticket_sla(self, ticket: Ticket) -> TicketSlaResponse:
        now = datetime.now(timezone.utc)
        created_at = ticket.created_at
        if created_at and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        response_due = ticket.response_due_at
        if response_due and response_due.tzinfo is None:
            response_due = response_due.replace(tzinfo=timezone.utc)

        resolution_due = ticket.resolution_due_at
        if resolution_due and resolution_due.tzinfo is None:
            resolution_due = resolution_due.replace(tzinfo=timezone.utc)

        # 1. Response status
        if ticket.first_response_at:
            resp_at = ticket.first_response_at
            if resp_at.tzinfo is None:
                resp_at = resp_at.replace(tzinfo=timezone.utc)
            if response_due and resp_at <= response_due:
                response_status = SlaStatus.MET
            else:
                response_status = SlaStatus.BREACHED
        elif response_due:
            if now > response_due:
                response_status = SlaStatus.BREACHED
            else:
                total_seconds = max((response_due - created_at).total_seconds(), 1)
                elapsed_seconds = (now - created_at).total_seconds()
                ratio = elapsed_seconds / total_seconds
                response_status = SlaStatus.AT_RISK if ratio >= 0.75 else SlaStatus.ON_TRACK
        else:
            response_status = SlaStatus.ON_TRACK

        # 2. Resolution status
        if ticket.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED] or ticket.resolved_at:
            res_at = ticket.resolved_at or now
            if res_at.tzinfo is None:
                res_at = res_at.replace(tzinfo=timezone.utc)
            if resolution_due and res_at <= resolution_due:
                resolution_status = SlaStatus.MET
            else:
                resolution_status = SlaStatus.BREACHED
        elif resolution_due:
            if now > resolution_due:
                resolution_status = SlaStatus.BREACHED
            else:
                total_seconds = max((resolution_due - created_at).total_seconds(), 1)
                elapsed_seconds = (now - created_at).total_seconds()
                ratio = elapsed_seconds / total_seconds
                resolution_status = SlaStatus.AT_RISK if ratio >= 0.75 else SlaStatus.ON_TRACK
        else:
            resolution_status = SlaStatus.ON_TRACK

        # 3. Overall status
        if response_status == SlaStatus.BREACHED or resolution_status == SlaStatus.BREACHED:
            overall_status = SlaStatus.BREACHED
        elif response_status == SlaStatus.AT_RISK or resolution_status == SlaStatus.AT_RISK:
            overall_status = SlaStatus.AT_RISK
        elif response_status == SlaStatus.MET and resolution_status == SlaStatus.MET:
            overall_status = SlaStatus.MET
        else:
            overall_status = SlaStatus.ON_TRACK

        return TicketSlaResponse(
            ticket_id=ticket.id,
            ticket_number=ticket.ticket_number,
            priority=ticket.priority,
            response_due_at=ticket.response_due_at,
            resolution_due_at=ticket.resolution_due_at,
            first_response_at=ticket.first_response_at,
            resolved_at=ticket.resolved_at,
            response_status=response_status,
            resolution_status=resolution_status,
            overall_status=overall_status,
        )

    def get_summary_status(self) -> SlaSummaryResponse:
        open_tickets = self.ticket_repo.get_open_tickets()
        counts = {
            SlaStatus.ON_TRACK: 0,
            SlaStatus.AT_RISK: 0,
            SlaStatus.BREACHED: 0,
            SlaStatus.MET: 0,
        }
        for ticket in open_tickets:
            sla_res = self.calculate_ticket_sla(ticket)
            counts[sla_res.overall_status] += 1

        return SlaSummaryResponse(
            total_open=len(open_tickets),
            on_track=counts[SlaStatus.ON_TRACK],
            at_risk=counts[SlaStatus.AT_RISK],
            breached=counts[SlaStatus.BREACHED],
            met=counts[SlaStatus.MET],
        )

    async def check_sla_breaches_and_warnings(self):
        """
        Background periodic checker for SLA warnings and breaches.
        """
        from app.services.notification_service import NotificationService

        notif_service = NotificationService(self.db)
        open_tickets = self.ticket_repo.get_open_tickets()
        now = datetime.now(timezone.utc)

        for ticket in open_tickets:
            sla_res = self.calculate_ticket_sla(ticket)
            recipient_id = ticket.assigned_to or ticket.created_by

            if sla_res.overall_status == SlaStatus.BREACHED:
                # Notify if breached
                await notif_service.create_and_send(
                    user_id=recipient_id,
                    title="SLA Breach Alert",
                    message=f"Ticket {ticket.ticket_number} has breached its SLA deadline.",
                    type=NotificationType.SLA_BREACH,
                    ticket_id=ticket.id,
                )
            elif sla_res.overall_status == SlaStatus.AT_RISK:
                # Notify if warning
                await notif_service.create_and_send(
                    user_id=recipient_id,
                    title="SLA Warning Alert",
                    message=f"Ticket {ticket.ticket_number} is approaching its SLA deadline (≥75% elapsed).",
                    type=NotificationType.SLA_WARNING,
                    ticket_id=ticket.id,
                )

    def list_rules(self) -> List[SlaRule]:
        rules = self.repo.list_rules()
        if not rules:
            # Seed defaults
            for priority, vals in DEFAULT_SLA_CONFIG.items():
                self.repo.update_rule(
                    priority=priority,
                    response_time=vals["response_time"],
                    resolution_time=vals["resolution_time"],
                )
            rules = self.repo.list_rules()
        return rules

    def update_rule(self, priority: TicketPriority, response_time: int, resolution_time: int) -> SlaRule:
        return self.repo.update_rule(priority, response_time, resolution_time)
