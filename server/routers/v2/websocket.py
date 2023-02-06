
from fastapi import APIRouter
from logger import log
from fastapi import  WebSocket, WebSocketDisconnect
from bl.chat import ChatBL
from routers.utils import Message
from typing import List

router = APIRouter(prefix="/chat/v2", tags=["Chat V2 - Websocket message"])

class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append((websocket, username))
        log.info(f"WebSocket connect username: {username}")

    def disconnect(self, websocket: WebSocket, username: str):
        self.active_connections.remove((websocket, username))

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection[0].send_json(data)   
             

manager = SocketManager() # global var
    
@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
   
    try:
        while True:
            msg_content = await websocket.receive_text() # Get data from connected user 
            # if msg_content:
                # msg_response = {"username": username, "message": msg_content}
                
            # save messga to DB:
            msg = Message(username=username, message=msg_content)
            ChatBL.create_message(msg)
                
            await manager.broadcast(f"{username}: {msg_content}") # Broadcast it to all connected users
            
           
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        log.warning(f"WebSocket disconnect username: {username}")
       