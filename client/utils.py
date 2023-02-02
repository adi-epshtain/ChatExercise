from pydantic import BaseModel

class Message(BaseModel):
    username: str
    message: str

class GetMsgException(Exception):
    "Raised when get messages got an server error"
    pass

class SendMsgException(Exception):
    "Raised when send message got an server error"
    pass


CHAT_SERVER = "http://localhost:8000"
