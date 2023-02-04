from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
  
    def __repr__(self):
        return f"user: {self.name}, id: {self.id}, room: {self.room_id}"
      
    
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(144), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    username = Column(String(50), ForeignKey("users.username"))

    def __repr__(self):
        return f"message: {self.message}"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    def __repr__(self):
        return f"room: {self.name}"