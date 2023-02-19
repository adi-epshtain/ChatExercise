from routers.utils import Message as MessageData, User as UserData
from logger import log
from sql.dals.message import MessageDal
from sql.dals.room import RoomDal
from sql.dals.user import UserDal
from sql.schemas import User, Room, Message

class CreateMsgException(Exception):
    "Raised when craete messages got an error"
    pass

class GetRoomException(Exception):
    "Raised when get room got an error"
    pass

class ChatBL:
    
    def get_rooms() -> list[Room]:
        rooms_list: list[Room] = RoomDal.get_rooms()
        return rooms_list
    
    def create_room(name: str) -> Room:
        room: Room = RoomDal.create_room(name)
        return room
    
    def create_message(msg: MessageData) -> Message:
        
        user: User = UserDal.get_user_by_name(msg.username)
        if user:
            MessageDal.create_message(msg.username, user.room_id, msg.message)
        else:
            log.error(f"trying to create a meesage but failed to get the user, user: {user}")
            raise CreateMsgException
    
    def get_messages(username: str) -> list[MessageData]:
        user: User = UserDal.get_user_by_name(username)
        msg_list_res = MessageDal.get_messages(user.room_id)

        msg_list = [{'message': msg.message, 'username': msg.username} for msg in msg_list_res]
            
        return msg_list

    def get_or_create_user(user: UserData) -> User:
        username = user.username
        room_name = user.room_name
        
        user: User = UserDal.get_user_by_name(username)
        if not user:
            log.info("create a new user")
            room: Room = RoomDal.get_room_by_name(room_name)
            if not room:
                log.error(f"trying to create a new user with not exist room , user: {user}, room: {room}")
                raise GetRoomException
            user: User = UserDal.create_user(username, room.id)
        return user