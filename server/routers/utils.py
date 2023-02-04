from pydantic import BaseModel

class Message(BaseModel):
    username: str
    message: str

class User(BaseModel):
    username: str
    room_name: str
