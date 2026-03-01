from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Todos,Users
from ..database import SessionLocal
from pydantic import BaseModel,Field
from .auth import get_current_user, bcrypt_context
from passlib.context import CryptContext

from .todos import TodoRequest

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
crypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')

class UserVerification(BaseModel):
    password: str
    new_password : str=Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_verification: UserVerification,
    db: db_dependency,
    user: user_dependency
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(
        Users.id == user.get('id')
    ).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(
        user_verification.password,
        user_model.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Invalid password")

    user_model.hashed_password = bcrypt_context.hash(
        user_verification.new_password
    )
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    db: db_dependency,
    user: user_dependency,
    phone_number: str
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(
        Users.id == user.get('id')
    ).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.phone_number = phone_number
    db.commit()





