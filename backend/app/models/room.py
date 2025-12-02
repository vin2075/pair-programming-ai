# backend/app/models/room.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from db.session import Base

class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(String(64), primary_key=True, index=True)
    last_code = Column(Text, default="")
    language = Column(String(32), default="python")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
