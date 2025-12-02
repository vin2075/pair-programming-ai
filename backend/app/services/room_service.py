# backend/app/services/room_service.py
import uuid
from sqlalchemy.orm import Session
from ..models.room import Room

class RoomService:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, language: str = "python") -> str:
        room_id = str(uuid.uuid4())[:8]
        room = Room(room_id=room_id, last_code="", language=language)
        self.db.add(room)
        self.db.commit()
        return room_id

    def get_room(self, room_id: str) -> Room | None:
        return self.db.query(Room).filter(Room.room_id == room_id).first()

    def update_code(self, room_id: str, code: str):
        room = self.get_room(room_id)
        if room:
            room.last_code = code
            self.db.add(room)
            self.db.commit()
