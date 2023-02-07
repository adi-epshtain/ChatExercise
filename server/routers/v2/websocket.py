
from fastapi import APIRouter
from logger import log
from fastapi import  WebSocket
from bl.chat import ChatBL
from routers.utils import Message

router = APIRouter(prefix="/chat/v2", tags=["Chat V2 - Websocket message"])

class SocketManager:
    def __init__(self):
        self.active_connections= []

    async def connect(self, websocket: WebSocket, room_name: str, username: str):
        await websocket.accept()
        self.active_connections.append((websocket, room_name, username))
        log.info(f"WebSocket connect username: {username} to: {room_name}")

    def disconnect(self, websocket: WebSocket, room_name: str, username: str):
        self.active_connections.remove((websocket, room_name, username))
        log.info(f"WebSocket disconnect username: {username} from room: {room_name}")

    async def broadcast(self, msg: str, room_name: str, username: str):
        log.info(f"WebSocket broadcast message of: {username} room: {room_name}")
        for connection in self.active_connections:
            await connection[0].send_json(msg) # send the suitable websocket the msg
             

manager = SocketManager() # global var
    
@router.websocket("/ws/{room_name}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, username: str):
    await manager.connect(websocket, room_name, username)
   
    try:
        while True:
            msg_content = await websocket.receive_text() # Get data from connected user 
          
            # save messga to DB:
            msg = Message(username=username, message=msg_content)
            ChatBL.create_message(msg)
                
            await manager.broadcast(f"{username}: {msg_content}", room_name, username) # Broadcast it to all connected users
             
    except Exception as e:
        manager.disconnect(websocket, room_name, username)
        log.warning(f"WebSocket disconnect username: {username} error: {e}")
       