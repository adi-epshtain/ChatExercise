""" This code is version2 of chat BL using websocket"""
import json
from logger import log
from utils import User, Room, GetUserException, GetRoomException
from proxy import ProxyUser, ProxyRoom
from constants import WEBSOCKET_URL
from websockets import connect, ConnectionClosed

def choose_room_name() -> str:
    rooms_list_data_response: list[Room] = ProxyRoom.get_rooms()
    if not rooms_list_data_response:
        log.error("Thre are no rooms")
        raise GetRoomException
    
    rooms_list: list[dict] = json.loads(rooms_list_data_response)

    for room in rooms_list:
        log.info(f"{room['id']}. {room['name']}")
    
    room_name: str = input("insert room name:")
    return room_name

async def chat_client():
    username: str = input("Hi there! Please insert your username:")
    # room_name: str = choose_room_name()
    room_name = "Backend"
    # username, room_name = "AdiE", "Backend"
    
    user = User(username=username, room_name=room_name)
    user_obj = ProxyUser.get_or_create_user(user)
    if not user_obj:
        raise GetUserException
    
    log.info(f"{username} Welcome to My chat")
    
    try:
        websocket_url_with_params = f"{WEBSOCKET_URL}/{username}"
        new_msg = input("Please insert your message:")
        async with connect(websocket_url_with_params) as websocket:
            while(True):
                await websocket.send(new_msg)
                new_msg = input("Please insert your message:")
                msg_received = await websocket.recv()
                log.info(msg_received)

    except ConnectionClosed:
        log.error(f"chat server connection closed")                
    except Exception as e:
        log.error(f"chat client failed with error: {e}")
        raise e
    