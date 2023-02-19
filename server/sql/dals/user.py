from ..models import User
from sql.database import session

class UserDal:
    
    """
    :return: user object or None case there is no user with this id
    """
    def get_user_by_id(user_id: int):
        return session.query(User).filter(User.id == user_id).first()

    """
    :return: user object or None case there is no user with this name
    """
    def get_user_by_name(username: str):
        user = session.query(User).filter(User.username == username).first()
        return user

    """
    :return: users object list or []
    """
    def get_users(skip: int = 0, limit: int = 100):
        return session.query(User).offset(skip).limit(limit).all()

    """
    :return: users object after created on DB
    """
    def create_user(username: str, room_id: int):
        db_user = User(username=username, room_id=room_id)
        session.add(db_user)
        session.commit() # flush changes to the database
        return db_user
