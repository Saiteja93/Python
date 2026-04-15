from datetime import datetime,timedelta,timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from passlib.context import CryptContext
import os

from typing_extensions import deprecated

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=["bycrpt"], deprecated="auto")


def hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain,hashed)


def create_access_token(username: str,user_id: int, user_role: str,expires_delta:timedelta):
    encode = {'sub': username, 'id': user_id, 'role': user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

