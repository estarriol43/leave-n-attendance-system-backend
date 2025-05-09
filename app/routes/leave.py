from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..crud import leave as leave_crud
from ..crud.leave import create_leave_request
from ..schemas.user import UserOut, TeamListResponse
from ..schemas.leave import LeaveRequestDetail, LeaveRequestOut, LeaveRequestCreate
from ..utils.dependencies import get_current_user
from ..models.user import User
from ..database import get_db

router = APIRouter(
    prefix="/api/leave-requests",
    tags=["leave-requests"]
)

@router.post("", response_model=LeaveRequestOut, status_code=status.HTTP_201_CREATED)
def request_leave(
    payload: LeaveRequestCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    try: 
        return create_leave_request(db, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{leave_request_id}", response_model=LeaveRequestDetail)
def get_leave_request_details(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific leave request by ID.
    """
    return leave_crud.get_leave_request_by_id(db, leave_request_id)



