import time
import json
from logger import log
from utils import Message
from proxy import send_message, get_messages
import urllib.request

def chat_client():
    log.info("hi chat_client!")
    # unsername: str = input("Hi there! Please insert your unsername:")
    
    # here using dummy data replace to get input from CLI:
    unsername = "Adi"
    new_messages = ["Hi all", "Good mornning", "I am here"]
    log.info(f"{unsername} Welcome to our chat")
    
    try:
        with urllib.request.urlopen('http://localhost:8000/api/docs'):
            while(True):
                # new_msg: str = input("Please insert your message:")
                # message_instance = Message(username=unsername, message=new_msg)
                for new_msg in new_messages:
                    message_instance = Message(username=unsername, message=new_msg)
                    
                    send_message(message_instance)

                msg_list_data_response: list[Message] = get_messages()

                msg_list: list[dict] = json.loads(msg_list_data_response)

                for msg in msg_list:
                    log.info(f"{msg['username']}: {msg['message']}")

                time.sleep(1) # change to 1 second
                log.info("---")        
    except Exception as e:
        log.error(f"chat client failed with error: {e}")
        raise e
    