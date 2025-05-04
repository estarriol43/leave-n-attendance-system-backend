from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..schemas.user import UserOut, TeamListResponse
from ..utils.dependencies import get_current_user
# from ..models.user import User
from ..database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/me", response_model=UserOut)
def get_my_profile( current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # temporary funciton without db
    user_id = current_user["id"]
    manager_id = current_user["manager_id"]
    department_id = current_user["department_id"]
    manager = user_crud.get_manager(manager_id) 
    department = user_crud.get_department(department_id)
    result = {
        "id": user_id,
        "employee_id": current_user["employee_id"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
        "email": current_user["email"],
        "department": department,
        "position": current_user["position"],
        "manager": manager,
        "hire_date": current_user["hire_date"],
        "is_manager": current_user["is_manager"]
    }
    return result 

"""
@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    manager_id = current_user.manager_id
    department_id = current_user.department_id
    manager = user_crud.get_manager(db, manager_id) 
    department = user_crud.get_department(db, department_id)
    result = {
        "id": user_id,
        "employee_id": current_user.employee_id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "department": department,
        "position": current_user.position,
        "manager": manager,
        "hire_date": current_user.hire_date,
        "is_manager": current_user.is_manager
    }
    return result 

@router.get("/team", response_model=TeamListResponse)
def get_my_team(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Only managers can access this resource.")
    members = user_crud.get_team_members(db, current_user.id)
    return {"team_members": members}
"""