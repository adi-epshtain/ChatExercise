from fastapi import APIRouter, HTTPException, status
from logger import log
from bl.chat import ChatBL
from logger import log

router = APIRouter(prefix="/room/v2", tags=["room v2"])


@router.get("/rooms", description="User retrieves a list of all previous messages")
def get_rooms() -> list:
    """
    Get all rooms
    :return: 200 OK with msg_list
    :exception: empty rooms list failed with NotFound (404)
    """
    rooms_list = ChatBL.get_rooms()
    
    if rooms_list:
        return rooms_list
    else:
        log.error("There are no rooms")
        raise HTTPException(status_code=404, detail="there are no rooms")  


@router.post("/room", status_code=status.HTTP_201_CREATED, description="create a new room")
def add_user(name: str):
    """
    Adding a new room to rooms DB table
    :return: 201 Created with room object
    :exception: Validation error failed with Unprocessable Entity (422)
                Any another exception failed with Internal server error (500) 
    """
    try:
        room = ChatBL.create_room(name)
        return room
    except Exception as e:
        log.error(f"Failed craete room with error: {e}")
        raise HTTPException(status_code=500, detail="failed create room") 

