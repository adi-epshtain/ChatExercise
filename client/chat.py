import time
import json
from logger import log
from utils import Message, User, Room, GetUserException, GetRoomException
from proxy import ProxyMsg, ProxyUser, ProxyRoom
import urllib.request
from constants import SECONDS_TO_SLEEP, SWAGGER_URL

def send_msg(username):
    new_msg: str = input("Please insert your message:")
    message_instance = Message(username=username, message=new_msg)
    ProxyMsg.send_message(message_instance)
    
def choose_room_name() -> str:
    rooms_list_data_response: list[Room] = ProxyRoom.get_rooms()
    if not rooms_list_data_response:
        log.error("Thre is no rooms")
        raise GetRoomException
    rooms_list: list[dict] = json.loads(rooms_list_data_response)

    for room in rooms_list:
        log.info(f"{room['id']}. {room['name']}")
    
    room_name: str = input("insert room name:")
    return room_name

def chat_client():
    username: str = input("Hi there! Please insert your username:")
    room_name = choose_room_name()
    
    user = User(username=username, room_name=room_name)
    user_obj = ProxyUser.get_or_create_user(user)
    if not user_obj:
        raise GetUserException
    
    log.info(f"{username} Welcome to My chat")
    
    try:
        with urllib.request.urlopen(SWAGGER_URL):
            while(True):
                send_msg(username)
        
                msg_list_data_response: list[Message] = ProxyMsg.get_messages(username)

                msg_list: list[dict] = json.loads(msg_list_data_response)

                for msg in msg_list:
                    log.info(f"{msg['username']}: {msg['message']}")

                time.sleep(SECONDS_TO_SLEEP) # change to 1 second
                log.info("---")        
    except Exception as e:
        log.error(f"chat client failed with error: {e}")
        raise e
    