from fastapi import FastAPI, Depends, HTTPException, Path,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from ..P_database import SessionLocal
from ..P_models import Todos
from .p_auth import get_current_user
from ..P_models import Todos


router = APIRouter(
    prefix="/admin",
    tags=['admin']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return db.query(Todos).all()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(user: user_dependency, db: db_dependency,todo_id: int):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    db.query(Todos).filter(Todos.id == todo_id).first().delete()

    db.commit()

