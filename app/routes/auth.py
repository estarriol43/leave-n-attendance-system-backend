from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schemas.user import UserLogin, Token
from ..crud import user as user_crud
from ..utils.auth import create_access_token
from ..utils.dependencies import login_form_schema
from ..database import get_db

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login", response_model=Token)
def login(login_data: login_form_schema, db: Session = Depends(get_db)):
    current_user = user_crud.authenticate_user(db, login_data.username, login_data.password)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = current_user.id
    department = user_crud.get_department(db, user_id)
    user = {
        "id": user_id,
        "employee_id": current_user.employee_id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "department":department,
        "position": current_user.position,
        "is_manager": current_user.is_manager        
    }
    token = create_access_token(data={"sub": str(user['id'])})
    
    cookie_response = JSONResponse(
        content={"access_token": token, "token_type": "bearer"}
    )
    cookie_response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,              # use False only in dev (http)
        samesite="Strict",        # or "Lax" if needed
        max_age=3600,             # 1 hour
        path="/"
    )
    return cookie_response

@router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out successfully"})
    
    # Clear the HTTP-only cookie by setting it to expire immediately
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="Strict",
        path="/"
    )
    
    return response