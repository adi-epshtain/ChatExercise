
from fastapi import FastAPI
from routers.v1.message import router as routerMessageV1
from routers.v2.message import router as routerMessageV2
from routers.v2.user import router as routerUserV2
from routers.v2.room import router as routerRoomV2

from logger import log

def create_app() -> FastAPI:

    app = FastAPI(
        title="Chat Server",
        description="A service for providing chat server. v2 implement with persistence DB",
        version="1.0.0",
        
        docs_url='/api/docs', # http://localhost:8000/api/docs
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json'
    )
    
    app.include_router(routerMessageV1)
    app.include_router(routerMessageV2)
    app.include_router(routerUserV2)
    app.include_router(routerRoomV2)
    
    return app


log.info("welcome to chat server")
app = create_app()
