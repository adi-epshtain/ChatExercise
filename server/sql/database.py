import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from logger import log
from constants import PRODUCTION
from .models import Room, User, Message


class SessionManager(object):
    """Manage SQLAlchemy sessions (Singleton design pattern)"""
    __instance = None
    
    def __init__(self):
        if SessionManager.__instance == None:
            # this is the only instance create do initialize the session manager: 
            SessionManager.__instance = self
            self.db_url = self._get_db_url()
            self.engine = create_engine(self.db_url, echo = True)
            self._prepare_models()
            log.debug(f"SessionManager after init & prepare_models")
      
    def _prepare_models(self):
        
        # Create a new MetaData object to store table metadata
        metadata = MetaData()
        
        log.debug(f"prepare_models process")
        
        Table(
        'rooms', metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('name', String(50), unique=True, index=True, nullable=False), 
        )
        
        Table(
        'users', metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('username', String(50), unique=True, index=True, nullable=False),
        Column('room_id', Integer, ForeignKey("rooms.id"))
        )

        Table(
        'messages', metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('message', String(144), nullable=False),
        Column('username', String(50), ForeignKey("users.username")),
        Column('room_id', Integer, ForeignKey("rooms.id"))
        )
        
        metadata.create_all(self.engine)   
           
    def _get_db_url(self):
        
        DEV_SERVER = "localhost:5432" # locally with venv
        load_dotenv()  # take environment variables from .env.
        app_mode = os.getenv("APP_MODE", PRODUCTION)
        log.debug(f"App mode: {app_mode}")
        
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        server = os.getenv("POSTGRES_SERVER", "db") # host name
        db_name = os.getenv("POSTGRES_DB", "postgres_db")
        server = os.getenv("POSTGRES_SERVER", "db") if app_mode is PRODUCTION else DEV_SERVER
        
        db_url = f"postgresql://{user}:{password}@{server}/{db_name}"
        log.debug(f"DB URL: {db_url}")
        return db_url
    
    def get_session(self):
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return session()

session_manager = SessionManager()
session = session_manager.get_session() # global var