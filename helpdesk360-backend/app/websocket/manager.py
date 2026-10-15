from datetime import datetime, timezone
from typing import Dict, List, Set, Any
from fastapi import WebSocket
from app.core.logging import logger
from app.models.enums import RoleEnum


class ConnectionManager:
    def __init__(self):
        # user_id -> Set[WebSocket]
        self.user_connections: Dict[int, Set[WebSocket]] = {}
        # ticket_id -> Dict[WebSocket, RoleEnum]
        self.ticket_connections: Dict[int, Dict[WebSocket, RoleEnum]] = {}

    async def connect_user(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(websocket)
        logger.debug(f"WS connected for user_id={user_id}. Active user conns={len(self.user_connections[user_id])}")

    def disconnect_user(self, user_id: int, websocket: WebSocket):
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        logger.debug(f"WS disconnected for user_id={user_id}")

    async def connect_ticket(self, ticket_id: int, websocket: WebSocket, role: RoleEnum):
        await websocket.accept()
        if ticket_id not in self.ticket_connections:
            self.ticket_connections[ticket_id] = {}
        self.ticket_connections[ticket_id][websocket] = role
        logger.debug(f"WS connected for ticket_id={ticket_id}, role={role}")

    def disconnect_ticket(self, ticket_id: int, websocket: WebSocket):
        if ticket_id in self.ticket_connections:
            self.ticket_connections[ticket_id].pop(websocket, None)
            if not self.ticket_connections[ticket_id]:
                del self.ticket_connections[ticket_id]
        logger.debug(f"WS disconnected for ticket_id={ticket_id}")

    async def send_to_user(self, user_id: int, event: str, data: Dict[str, Any]):
        if user_id not in self.user_connections:
            return
        payload = {
            "event": event,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        dead_conns = set()
        for ws in self.user_connections[user_id]:
            try:
                await ws.send_json(payload)
            except Exception as e:
                logger.debug(f"Error sending to user WS: {e}")
                dead_conns.add(ws)

        for ws in dead_conns:
            self.user_connections[user_id].discard(ws)

    async def broadcast_to_ticket(
        self,
        ticket_id: int,
        event: str,
        data: Dict[str, Any],
        is_internal_note: bool = False,
    ):
        if ticket_id not in self.ticket_connections:
            return

        payload = {
            "event": event,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        dead_conns = set()
        for ws, role in self.ticket_connections[ticket_id].items():
            # Filter internal note from employees
            if is_internal_note and role != RoleEnum.TECHNICIAN:
                continue

            try:
                await ws.send_json(payload)
            except Exception as e:
                logger.debug(f"Error broadcasting to ticket WS: {e}")
                dead_conns.add(ws)

        for ws in dead_conns:
            self.ticket_connections[ticket_id].pop(ws, None)


ws_manager = ConnectionManager()
