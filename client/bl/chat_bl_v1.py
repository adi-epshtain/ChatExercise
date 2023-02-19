"""
    Version1 of chat BL using Rest API each 1 second get all messages and print them.
    This code currently not in use (using chat_bl_v2 with webscoket)
"""
import time
import json
from logger import log
from utils import Message, User, Room, GetUserException, GetRoomException
from proxy import ProxyMsg, ProxyUser, ProxyRoom
import urllib.request
from constants import SECONDS_TO_SLEEP, SWAGGER_URL

class ChatBLV1:
    def __init__(self) -> None:
        self.username = None
    
    async def send_msg(self):
        new_msg: str = input("Please insert your message:")
        message_instance = Message(username=self.username, message=new_msg)
        await ProxyMsg.send_message(message_instance)
        
    async def choose_room_name(self) -> str:
        rooms_list_data_response: list[Room] = await ProxyRoom.get_rooms()
        if not rooms_list_data_response:
            log.error("Thre is no rooms")
            raise GetRoomException
        rooms_list: list[dict] = json.loads(rooms_list_data_response)

        for room in rooms_list:
            log.info(f"{room['id']}. {room['name']}")
        
        room_name: str = input("insert room name:")
        return room_name

    async def chat_client(self):
        username: str = input("Hi there! Please insert your username:")
        room_name = await self.choose_room_name()
        
        user = User(username=username, room_name=room_name)
        user_obj = await ProxyUser.get_or_create_user(user)
        if not user_obj:
            raise GetUserException
        
        log.info(f"{username} Welcome to My chat")
        
        try:
            with urllib.request.urlopen(SWAGGER_URL):
                while(True):
                    await self.send_msg(self.username)

                    # using Rest API to get and print all room messsages:
                    msg_list_data_response: list[Message] = await ProxyMsg.get_messages(username)
                    msg_list: list[dict] = json.loads(msg_list_data_response)
                    for msg in msg_list:
                        log.info(f"{msg['username']}: {msg['message']}")

                    time.sleep(SECONDS_TO_SLEEP)
                    log.info("---")        
        except Exception as e:
            log.error(f"chat client failed with error: {e}")
            raise e
        