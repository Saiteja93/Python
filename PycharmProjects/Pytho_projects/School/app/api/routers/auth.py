
from fastapi import APIRouter
from typing import Annotated
from starlette import status
from pydantic import BaseModel
from ..dependences.deps import db_dependency
from ...db.models import Users
from ...core.security import pwd_context
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Toke(BaseModel):
    access_token : str
    token_type: str




@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=pwd_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number

    )
    db.add(create_user_model)
    db.commit()


@router.post("/login_token", response_model=Toke)
async def login_token_access(db:db_dependency, form_data = Annotated):
