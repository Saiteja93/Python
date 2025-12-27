
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pycparser.ply.lex import TOKEN, Token
from pydantic import BaseModel
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt


router = APIRouter()
SECRET_KEY = 'e13f82a967ab0e7623a9fbec4719d06303b309e03e36685c67f821c41ddfd32d'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')

class CreateUserRequest(BaseModel):
    username : str
    email: str
    first_name: str
    last_name : str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db ):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub':username,'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request : CreateUserRequest
                      ):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()



@router.post('/token' ,response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # Raise proper HTTP 401 error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(username=user.username, user_id=user.id, expires_delta=timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

