from pydantic import BaseModel

class Message(BaseModel):
    username: str
    message: str

class GetMsgException(Exception):
    "Raised when get messages got an server error"
    pass

class GetUserException(Exception):
    "Raised when get messages got an server error"
    pass

class GetRoomException(Exception):
    "Raised when get room got an server error"
    pass

class SendMsgException(Exception):
    "Raised when send message got an server error"
    pass

class Room(BaseModel):
    id: str
    name: str

class User(BaseModel):
    username: str
    room_name: str