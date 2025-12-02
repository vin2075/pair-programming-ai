# backend/app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .routers import rooms, autocomplete
from db.session import init_db, SessionLocal
from .ws_manager import manager
from .services.room_service import RoomService
import json
import os

app = FastAPI(title="Pair Coding API")

# allow localhost during dev and production origin via env
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router, prefix="")
app.include_router(autocomplete.router, prefix="")

@app.on_event("startup")
def on_startup():
    init_db()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    db = SessionLocal()
    await manager.connect(room_id, websocket)
    try:
        # if no in-memory code present load from DB
        if manager.get_room_code(room_id) == "":
            service = RoomService(db)
            room = service.get_room(room_id)
            if room:
                manager.set_room_code(room_id, room.last_code or "")
        # send initial state
        await websocket.send_text(json.dumps({"type": "initial", "code": manager.get_room_code(room_id)}))

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get("type") == "code_update":
                code = payload.get("code", "")
                # update in-memory
                manager.set_room_code(room_id, code)
                # persist to DB
                service = RoomService(db)
                service.update_code(room_id, code)
                # broadcast to others
                await manager.broadcast(room_id, {"type": "code_update", "code": code}, exclude=websocket)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    finally:
        db.close()
