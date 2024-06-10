from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from models import User
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated



bcrpyt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")



SECRET_KEY = "42da85de9512b12fecdda1d7bdaa0b34"
ALGORITHM = 'HS256'

def authenticate_user(username:str, password:str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrpyt.verify(password, user.hashed_pasword):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'ctrl': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("ctrl")
        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")