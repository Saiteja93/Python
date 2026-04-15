

from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from datetime import timedelta, datetime, timezone
import bcrypt
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..P_database import SessionLocal
from ..P_models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY = '9477a1262a5e02f05186c1719b5d72e0a299fb77b7cad173240f1b797e4ed98a'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name : str
    last_name : str
    password: str = Field(max_length=72)
    role: str


class Toke(BaseModel):
    access_token: str
    token_type : str


def create_access_token(username:str, user_id: int, role: str, expires_delta: timedelta ):
    encode = {'sub': username, 'id': user_id,  'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Token Payload is -> {payload}")
        username: str = payload.get('sub')
        user_id: str= payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate user')
        return {'username':username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "could not validate user")


@router.post("/creation", status_code=status.HTTP_201_CREATED)
async def create_user( db: db_dependency, user_request: CreateUserRequest):
    new_data = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        hashed_password = bcrypt_context.hash(user_request.password),
        is_active = True,
        role = user_request.role,

    )
    db.add(new_data)
    db.commit()

    return {"message": "Data created successfully"}

@router.post("/token", response_model=Toke)
async def login_for_access(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role,timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
