from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing import Annotated

from ...db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()


db_dependency =Annotated[Session, Depends(get_db)]
oAuth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oAuth2_bearer)]):
    try;






