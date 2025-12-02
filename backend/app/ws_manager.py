# backend/app/ws_manager.py
from typing import Dict, Set, Optional
from starlette.websockets import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, Set[WebSocket]] = {}
        self.room_state: Dict[str, str] = {}

    async def connect(self, room_id: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(room_id, set()).add(ws)

    def disconnect(self, room_id: str, ws: WebSocket):
        conns = self.active.get(room_id)
        if conns and ws in conns:
            conns.remove(ws)
            if not conns:
                # keep the in-memory state for a short time (could also clear)
                pass

    async def broadcast(self, room_id: str, message: dict, exclude: Optional[WebSocket] = None):
        conns = list(self.active.get(room_id, []))
        data = json.dumps(message)
        for conn in conns:
            if conn is exclude:
                continue
            try:
                await conn.send_text(data)
            except Exception:
                # ignore single-client errors
                pass

    def set_room_code(self, room_id: str, code: str):
        self.room_state[room_id] = code

    def get_room_code(self, room_id: str) -> str:
        return self.room_state.get(room_id, "")

manager = ConnectionManager()
