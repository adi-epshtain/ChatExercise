import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from logger import log
from sqlalchemy.ext.declarative import declarative_base

ResultModelBase = declarative_base()
__all__ = ('SessionManager',)

class SessionManager(object):
    """Manage SQLAlchemy sessions."""

    def __init__(self):
        self.prepared = False
        self.db_url = self.get_db_url()
        self.engine = create_engine(self.db_url, echo = True)
        self.metadata = MetaData()
        

        Table(
        'users', self.metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('username', String(50), unique=True, index=True, nullable=False),
        Column('room_id', Integer, ForeignKey("rooms.id"))
        )

        Table(
        'messages', self.metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('message', String(144), nullable=False),
        Column('username', String(50), ForeignKey("users.username")),
        Column('room_id', Integer, ForeignKey("rooms.id"))
        )

        Table(
        'rooms', self.metadata, 
        Column('id', Integer, primary_key = True, index=True), 
        Column('name', String(50), unique=True, index=True, nullable=False), 
        )

        self.metadata.create_all(self.engine)   

    def prepare_models(self, engine):
        if not self.prepared:
            ResultModelBase.metadata.create_all(engine)
            self.prepared = True
       
    def get_session(self):
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.prepare_models(self.engine)
        return session()
    
    def get_db_url(self):
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        server = os.getenv("POSTGRES_SERVER", "db") # host name
        db_name = os.getenv("POSTGRES_DB", "postgres_db")
        
        # server = "localhost:5432" # locally with venv
        
        db_url = f"postgresql://{user}:{password}@{server}/{db_name}"
        log.info(f"db_url={db_url}")
        return db_url

from sql.database import SessionManager
session_manager = SessionManager()
session = session_manager.get_session()