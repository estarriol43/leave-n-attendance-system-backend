from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from ..database import get_db
from ..crud.user import get_user_by_id
from .auth import SECRET_KEY, ALGORITHM
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
login_form_schema = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_current_user(token: str = Depends(oauth2_scheme)):
    # temporary function without db
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials in gcu",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

"""
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user
    """