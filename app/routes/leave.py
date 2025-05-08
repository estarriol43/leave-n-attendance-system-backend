from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..schemas.user import UserOut, TeamListResponse
from ..utils.dependencies import get_current_user
from ..models.user import User
from ..database import get_db

router = APIRouter(
    prefix="/api/leave",
    tags=["leave-requests"]
)

