""" Version2 of chat BL using websocket"""
import json
import asyncio
from logger import log
from utils import User, Room, GetUserException, GetRoomException
from proxy import ProxyUser, ProxyRoom
from constants import WEBSOCKET_URL
from websockets import connect

class ChatBLV2:
    def __init__(self) -> None:
        self.username = None
        self.room_name = None
    
    async def init_username_and_room(self):
        self.username: str = input("Hi there! Please insert your username:")
        await self.choose_room_name()

        # debug only:
        # self.username = "AdiE"
        # self.room_name = "Backend"
        
        user = User(username=self.username, room_name=self.room_name)
        user_obj = await ProxyUser.get_or_create_user(user)
        if not user_obj:
            raise GetUserException
        

    async def choose_room_name(self):
        rooms_list_data_response: list[Room] = await ProxyRoom.get_rooms()
        if not rooms_list_data_response:
            log.error("Thre are no rooms")
            raise GetRoomException
        
        rooms_list: list[dict] = json.loads(rooms_list_data_response)

        for room in rooms_list:
            log.info(f"{room['id']}. {room['name']}")
        
        self.room_name: str = input("insert room name:")

    async def chat_client(self):
    
        await self.init_username_and_room()
        log.info(f"{self.username} Welcome to My chat")
        
        while True:
            try:
                websocket_url_with_params = f"{WEBSOCKET_URL}/{self.room_name}/{self.username}"
                
                async with connect(websocket_url_with_params) as websocket:
                    while(True):
                        new_msg = input("Please insert your message:")
                        await websocket.send(new_msg)      
                        msg_received = await asyncio.wait_for(websocket.recv(), timeout=10)
                        log.info(msg_received)            
            except Exception as e:
                log.warning(f"Websocket connection failed, error: {e}. Retrying reconnect in 1 second ...")
                await asyncio.sleep(1)

               
        