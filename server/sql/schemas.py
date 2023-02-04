from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    room_id: int
    

    class Config:
        orm_mode = True # tells Pydantic to map the models to ORM objects

class Message(BaseModel):
    id: int
    message: str
    username: str
    room_id: int

    class Config:
        orm_mode = True

class Room(BaseModel):
    id: int
    name: str
    

    class Config:
        orm_mode = True