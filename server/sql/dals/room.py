
from ..models import Room
from sql.database import session

class RoomDal:
    
    """
    :return: room object or None case there is no room with this name
    """
    def get_room_by_name(name: str):
        return session.query(Room).filter(Room.name == name).first()

    """
    :return: room object or None case there is no user with this name
    """
    def get_rooms(skip: int = 0, limit: int = 100):
        
        rooms =  session.query(Room).offset(skip).limit(limit).all()
        return rooms

    """
    :return: room object after created on DB
    """
    def create_room(name: str):
        db_room = Room(name=name)
        session.add(db_room)
        session.commit() # flush changes to the database
        
        return db_room

