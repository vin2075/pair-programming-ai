# backend/app/routers/rooms.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from ..services.room_service import RoomService
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateRoomResp(BaseModel):
    roomId: str

@router.post("/rooms", response_model=CreateRoomResp)
def create_room(language: str = "python", db: Session = Depends(get_db)):
    service = RoomService(db)
    room_id = service.create_room(language)
    return {"roomId": room_id}

@router.get("/rooms/{room_id}")
def get_room(room_id: str, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "roomId": room.room_id,
        "last_code": room.last_code or "",
        "language": room.language
    }
