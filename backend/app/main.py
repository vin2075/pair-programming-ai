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

# -------------------------------------------------
# CORS Configuration
# -------------------------------------------------

# 1️⃣ Default origins (local dev)
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# 2️⃣ Read allowed frontend origins from env variable
# Multiple URLs can be separated by commas
FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    ",".join(default_origins)  # fallback to localhost if not set
)

# 3️⃣ Build list of origins
origins = [origin.strip() for origin in FRONTEND_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow only specified origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(rooms.router, prefix="")
app.include_router(autocomplete.router, prefix="")

# -------------------------------------------------
# Startup
# -------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()

# -------------------------------------------------
# WebSocket Endpoint
# -------------------------------------------------
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    db = SessionLocal()
    await manager.connect(room_id, websocket)
    try:
        # Load code from DB if in-memory is empty
        if manager.get_room_code(room_id) == "":
            service = RoomService(db)
            room = service.get_room(room_id)
            if room:
                manager.set_room_code(room_id, room.last_code or "")

        # Send initial state
        await websocket.send_text(
            json.dumps({"type": "initial", "code": manager.get_room_code(room_id)})
        )

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get("type") == "code_update":
                code = payload.get("code", "")
                # Update in-memory
                manager.set_room_code(room_id, code)
                # Persist to DB
                service = RoomService(db)
                service.update_code(room_id, code)
                # Broadcast to others
                await manager.broadcast(room_id, {"type": "code_update", "code": code}, exclude=websocket)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    finally:
        db.close()
