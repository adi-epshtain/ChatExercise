from fastapi import APIRouter, HTTPException, status, Body
from routers.utils import Message as MessageData
from logger import log
from bl.chat import ChatBL

router = APIRouter(prefix="/chat/v2", tags=["chat v2"])


@router.post("/message", status_code=status.HTTP_201_CREATED, description="user sends request with username and message")
def send_message(msg: MessageData = Body(
        example={
            "username": "AdiE",
            "message": "Hi all",
        },
    ),) -> MessageData:
    """
    Adding a new msg to messages DB table
    :return: 201 Created with msg object
    :exception: Validation error failed with Unprocessable Entity (422)
                Any another exception failed with Internal server error (500) 
    """
    try:
        ChatBL.create_message(msg)
        return msg
    except Exception as e:
        log.error("Failed send message with error", e)
        raise HTTPException(status_code=500, detail="failed send message") 

@router.get("/messages", description="User retrieves a list of all previous messages")
def get_messages(username: str) :#-> list[MessageData]:
    """
    Get all messages related to user room
    :return: 200 OK with msg_list
    :exception: empty message list failed with NotFound (404)
    """
    msg_list = ChatBL.get_messages(username)
    
    if msg_list:
        return msg_list
    else:
        log.error("There are no messages")
        raise HTTPException(status_code=404, detail="there are no messages")  


