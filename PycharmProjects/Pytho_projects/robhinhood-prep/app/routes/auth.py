from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.models import Users
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#JWT config
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_dependency = Annotated[Session,Depends(get_db)]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

#Creating access token


##Registering user POST endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate, db: db_dependency):
    existing_user = db.query(Users).filter(
        Users.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    #Hash password
    hashed_password = bcrypt_context.hash(user.password)

    #create new user
    new_user = Users(
        username = user.username,
        email = user.email,
        hashed_password=hashed_password,
        role = "user",
        is_active=True
    )
    db.add(new_user)
    db.commit()

    return {"message": "user registered successfully"}
