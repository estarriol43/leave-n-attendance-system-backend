from sqlalchemy.orm import Session
from sqlalchemy import select
from ..utils.auth import verify_password
from typing import List
from ..models.user import User
from ..models.department import Department


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
        "position": "senior engineer",
        "is_manager": True 
    },
    {
        "id": 2,
        "employee_id": "Q1",
        "first_name": "alice",
        "last_name": "wang",
        "email": "alice@ntu",
        "password": "mypass",
        "department": fake_db_department[0],
        "position": "engineer",
        "is_manager": False
    },
]



# def authenticate_user( email: str, password: str):
#     # temporary function without authentiacation and db
#     # get user
#     if(fake_db_user[0]["email"]!= email):
#         return None
#     # check passowrd:
#     if(fake_db_user[0]["password"]!= password):
#         return None
#     return fake_db_user[0]


def get_user_by_email(db: Session, email: str):
    res = db.query(User).filter(User.email == email).first()
    return res

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash): 
        return None
    return user
    


# def get_user_by_id(user_id: int):
#     # temporary function without db
#     if(fake_db_user[0]['id'] != user_id):
#         return None
#     user = {
#         "department_id": 1,
#         "id": 1,
#         "employee_id": "Q1",
#         "first_name": "owen",
#         "last_name": "chen",
#         "email": "owen@ntu",
#         "password_hash": "mypass",
#         "position": "engineer",
#         "manager_id": 2,
#         "hire_date": "2025/05/03",
#         "is_manager": True,
#         "annual_leave_quota": 3,
#         "sick_leave_quota": 3,
#         "public_holiday_quota": 3
#     }
#     return user 

# def get_team_members(manager_id: int):
#    # temporary function without db
#     if(fake_db_user[0]['id'] != manager_id):
#         return None
#     user = [{
#         "department_id": 1,
#         "id": 2,
#         "employee_id": "Q2",
#         "first_name": "alice",
#         "last_name": "wang",
#         "email": "alice@ntu",
#         "password_hash": "mypass",
#         "position": "engineer",
#         "manager_id": 1,
#         "hire_date": "2025/05/03",
#         "is_manager": True,
#         "annual_leave_quota": 3,
#         "sick_leave_quota": 3,
#         "public_holiday_quota": 3
#     }]
#     return user 

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_team_members(db: Session, manager_id: int) -> List[User]:
    return db.query(User).filter(User.manager_id == manager_id).all()

# def get_manager(manager_id: int):
#     # temporary function without db
#     if manager_id == 2: 
#         result = {
#             "id": 2,
#             "first_name": "alice",
#             "last_name": "wang"
#         }
#         return result
#     return None

# def get_department(department_id: int):
#     # temporary funciton without db
#     if department_id == 1:
#         result = {
#             "id": 1,
#             "name": "RD"
#         }
#         return result
#     return None

def get_manager(db: Session, manager_id: int):
    stmt = select(User.id, User.first_name, User.last_name).where(User.id == manager_id)
    return db.execute(stmt).first()

def get_department(db: Session, department_id: int):
    stmt = select(Department.id, Department.name)
    return db.execute(stmt).first()