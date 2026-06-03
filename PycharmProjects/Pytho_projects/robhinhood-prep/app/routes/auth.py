from fastapi import APIRouter,HTTPException, Depends,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.models import Users
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

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

#
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name : str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

#Creating access token
def create_access_token(user_id: int, username: str, role: str):
    payload = {
        "user_id":user_id,
        "username":username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#Login endpoint
@router.post("/login")
@limiter.limit("5/minute")
async def login( request: Request,db: db_dependency,
                form_data : OAuth2PasswordRequestForm = Depends()
                ):
    db_user = db.query(Users).filter(
        (Users.username == form_data.username)|
        (Users.email == form_data.username)
        ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not bcrypt_context.verify(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(db_user.id, db_user.username, db_user.role)

    return {
        "access_token":token,
        "token_type": "bearer"
    }

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
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()

    return {"message": "user registered successfully"}
