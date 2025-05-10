from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from ..database import get_db
from ..crud.user import get_user_by_id
from .auth import SECRET_KEY, ALGORITHM
from typing import Annotated
import logging

# 取得模組的日誌記錄器
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
login_form_schema = Annotated[OAuth2PasswordRequestForm, Depends()]

    

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Try to get token from cookie first
    token = request.cookies.get("access_token")
    
    # If no token in cookie, check Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        logger.debug(f"No token in cookie, checking Authorization header: {auth_header}")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            logger.debug(f"Found token in Authorization header: {token[:10]}...")
    
    if not token:
        logger.warning(f"Authentication failed: No token provided in request from {request.client.host}")
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        logger.debug(f"Decoding token: {token[:10]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning(f"Authentication failed: Token missing 'sub' field - {token[:15]}...")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.debug(f"Token decoded successfully for user_id: {user_id}")
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)} - Token: {token[:15]}...")
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(db, user_id)
    if user is None:
        logger.error(f"User with id {user_id} not found in database")
        raise HTTPException(status_code=404, detail="User not found")

    logger.debug(f"User authenticated: {user.email} (ID: {user.id})")
    return user