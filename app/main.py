
from fastapi import FastAPI
from app.routers import chat
from app.logging import log

app = FastAPI(
    title="Chat Server",
    description="A service for providing chat server",
    version="1.0.0",
)

app.include_router(chat.router)


log.info("welcome to chat server")
