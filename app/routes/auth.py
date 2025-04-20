# app/routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
