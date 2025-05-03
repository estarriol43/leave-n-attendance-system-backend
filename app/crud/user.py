from sqlalchemy.orm import Session
from ..utils.auth import verify_password
# from ..models.user import User

fake_db_department = [
    {
        "id": 1,
        "name": "RD"
    },
]

fake_db_user = [
    {
        "id": 1,
        "employee_id": "Q1",
        "first_name": "owen",
        "last_name": "chen",
        "email": "owen@ntu",
        "password": "mypass",
        "department": fake_db_department[0],
        "position": "engineer",
        "is_manager": True
    },
]



def authenticate_user( email: str, password: str):
    # temporary function without authentiacation and db
    # get user
    if(fake_db_user[0]["email"]!= email):
        return None
    # check passowrd:
    if(fake_db_user[0]["password"]!= password):
        return None
    return fake_db_user[0]

"""
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
    
    """