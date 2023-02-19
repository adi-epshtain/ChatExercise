from logger import log
import requests
from fastapi.encoders import jsonable_encoder
from utils import Message, Room, GetMsgException, GetRoomException, SendMsgException, User
from constants import GET_MSG_URL, SEND_MSG_URL, GET_USER_URL, GET_ROOMS_URL

class ProxyMsg:
    async def get_messages(username: str) -> list[Message]:
        """
        :return: list of messages or empty list case no messages
        :exception: GetMsgException
        """
        log.debug(f"client send GET request with url {GET_MSG_URL}")
        
        try:
            request_params = {"username": username}
            resp = requests.get(url=GET_MSG_URL, params=request_params, timeout=60, allow_redirects=False)
        except requests.ConnectionError:
            log.error("Server Connection Error")
            raise
        
        if resp.status_code == 404:
            log.warning("no messages")
            return []
        elif resp.status_code != 200:
            raise GetMsgException("Sorry, get messages failed")
        else:
            return resp.text
    
    async def send_message(msg: Message):
        """
        send a new message
        """
        log.debug(f"client send POST request with url {SEND_MSG_URL}")
        
        json_compatible_msg_data: dict = jsonable_encoder(msg)
        
        try:
            resp = requests.post(url=SEND_MSG_URL, json=json_compatible_msg_data, timeout=60, allow_redirects=False)
        except requests.ConnectionError as e:
            log.error("Server Connection Error")
            raise
        if resp.status_code == 422:
            raise SendMsgException("Sorry, Invalid message")

class ProxyUser:
    async def get_or_create_user(user: User):
        """
        get or craete a new user
        """
        log.debug(f"client send POST request with url {GET_USER_URL}")
        
        json_compatible_user_data: dict = jsonable_encoder(user)
        try:
            resp = requests.post(url=GET_USER_URL, json=json_compatible_user_data, timeout=60, allow_redirects=False)
        except requests.ConnectionError:
            log.error("Server Connection Error")
            raise
        if resp.status_code == 422:
            raise SendMsgException("Sorry, Invalid user data")
        return resp


class ProxyRoom:
    async def get_rooms() -> list[Room]:
        """
        :return: list of rooms or empty list case no rooms
        :exception: GetMsgException
        """
        log.debug(f"client send GET request with url {GET_ROOMS_URL}")
        
        try:
            rooms_list_res = requests.get(url=GET_ROOMS_URL, timeout=60, allow_redirects=False)
        except requests.ConnectionError:
            log.error("Server Connection Error")
            raise
            
        if rooms_list_res.status_code == 404:
            log.warning("no messages")
            return []
        elif rooms_list_res.status_code != 200:
            raise GetRoomException("Sorry, get rooms failed")
        else:
            return rooms_list_res.text
        