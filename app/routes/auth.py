from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import user
from ..crud import user as user_crud
from ..crud.auth import create_access_token

router = APIRouter(
    prefix="/api/auth"
)


@router.post("/login", response_model=user.TokenResponse)
def login(login_data: user.UserLogin):
    # temporary login funciton without db and token
    user = user_crud.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = "mytoken"
    return {"token": token, "user": user}

"""
@router.post("/login", response_model=user.TokenResponse)
def login(login_data: user.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"token": token, "user": user}
"""

@router.post("/logout")
def logout():
    # 若不處理 token 黑名單，前端清除 token 即完成
    return {"message": "Logged out successfully"}