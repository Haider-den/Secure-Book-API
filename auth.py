from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import database, crud, schemas
import os

SECRET_KEY = os.getenv('SECRET_KEY','change_this_secret_for_demo')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES','15'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class UserObj:
    def __init__(self, username, roles):
        self.username = username
        self.roles = roles

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles_raw: str = payload.get("roles","reader")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = database.SessionLocal()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise credentials_exception
    user.roles = roles_raw.split(',') if isinstance(roles_raw, str) else roles_raw
    return user
