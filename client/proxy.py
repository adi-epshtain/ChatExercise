from logger import log
import requests
from fastapi.encoders import jsonable_encoder
from utils import Message, GetMsgException, SendMsgException, CHAT_SERVER

def get_messages() -> list[Message]:
    """
    :return: list of messages or empty list case no messages
    :exception: GetMsgException
    """
    url = f"{CHAT_SERVER}/chat/messages"
    log.debug(f"client send GET request with url {url}")
    
    resp = requests.get(url=url, timeout=60, allow_redirects=False)
 
    if resp.status_code == 404:
        log.warning("no messages")
        return []
    elif resp.status_code != 200:
        raise GetMsgException("Sorry, get messages failed")
    else:
        return resp.text

def send_message(msg: Message):
    """
    send a new message
    """
    url = f"{CHAT_SERVER}/chat/message"
    log.debug(f"client send POST request with url {url}")
    
    json_compatible_msg_data: dict = jsonable_encoder(msg) # dict
    
    resp = requests.post(url=url, json=json_compatible_msg_data, timeout=60, allow_redirects=False)
    if resp.status_code == 422:
        raise SendMsgException("Sorry, Invalid message")
