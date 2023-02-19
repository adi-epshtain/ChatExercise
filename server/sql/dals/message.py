from ..models import Message
from sql.database import session

class MessageDal:
    
    """
    filter all messages related specfic room
    :return: message object list or [] 
    """
    def get_messages(room_id: int) -> list[Message]:
        messages_res = session.query(Message).filter(Message.room_id == room_id).all()
        return messages_res
    
    """
    :return: message object after created on DB
    """
    def create_message(username: str, room_id: int, message: str) -> Message:
        db_message = Message(message=message, username=username, room_id=room_id)
        session.add(db_message)
        
        session.commit() # flush changes to the database
        return db_message

