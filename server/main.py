
from fastapi import FastAPI
from routers import chat
from logger import log

app = FastAPI(
    title="Chat Server",
    description="A service for providing chat server",
    version="1.0.0",
    
    docs_url='/api/docs', # http://localhost:8000/api/docs
    redoc_url='/api/redoc',
    openapi_url='/api/openapi.json'
)

app.include_router(chat.router)

log.info("welcome to chat server")
