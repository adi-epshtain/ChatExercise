from fastapi import APIRouter, HTTPException, status, Body
from routers.models import Message
from logger import log

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

msg_list = []

@router.post("/message", status_code=status.HTTP_201_CREATED, description="user sends request with username and message")
def send_message(msg: Message = Body(
        example={
            "username": "AdiE",
            "message": "Hi all",
        },
    ),) -> Message:
    """
    Adding a new msg to msg_list
    :return: 201 Created with msg object
    :exception: Validation error failed with Unprocessable Entity (422)
                Any another exception failed with Internal server error (500) 
    """
    global msg_list
    
    try:
        msg_list.append(msg)
        return msg
    except Exception as e:
        log.error("Failed send message with error", e)
        raise HTTPException(status_code=500, detail="failed send message") 

@router.get("/messages", description="User retrieves a list of all previous messages")
def get_messages() -> list[Message]:
    """
    Get msg_list
    :return: 200 OK with msg_list
    :exception: empty message list failed with NotFound (404)
    """
    global msg_list
    
    if msg_list:
        return msg_list
    else:
        log.error("There are no messages")
        raise HTTPException(status_code=404, detail="there are no messages")  


