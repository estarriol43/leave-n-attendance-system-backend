from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas.leave_balance import LeaveBalanceResponse
from ..crud.leave_balance import get_leave_balances
from ..utils.dependencies import get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/api/leave-balances", 
    tags=["Leave Balance"]
)


@router.get("", response_model=LeaveBalanceResponse)
def read_my_leave_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_leave_balances(db, current_user.id)


@router.get("/{user_id}", response_model=LeaveBalanceResponse)
def read_user_leave_balance(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_leave_balances(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
