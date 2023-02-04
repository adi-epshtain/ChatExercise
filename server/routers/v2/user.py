from fastapi import APIRouter, HTTPException, status, Body
from routers.utils import User as UserData
from logger import log
from bl.chat import ChatBL
from logger import log

router = APIRouter(prefix="/user/v2", tags=["user v2"])


@router.post("/user", status_code=status.HTTP_201_CREATED, description="get or create a new user on specfic room")
def add_user(user: UserData = Body(
        example={
            "username": "AdiE",
            "room_name": "AI",
        },
    ),):
    """
    Adding a new user to users DB table, username unique. case exist user with this name return it, else create a new one.
    :return: 201 Created with user object
    :exception: Validation error failed with Unprocessable Entity (422)
                Any another exception failed with Internal server error (500) 
    """
    try:
        user = ChatBL.get_or_create_user(user)
        return user
    except Exception as e:
        log.error(f"Failed get or craete user with error: {e}")
        raise HTTPException(status_code=500, detail="failed get/create user") 
