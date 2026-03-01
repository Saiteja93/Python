from fastapi import Depends, HTTPException, Path, Query,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from P_models import Todos
from P_database import SessionLocal, engine
from starlette import status
from pydantic import Field, BaseModel
from datetime import datetime
from .p_auth import get_current_user


router = APIRouter(prefix="/admin", tags=["admin"])

current_year = datetime.now().year

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code = status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code = 401, detail= 'Authentication failed')

    return db.query(Todos).all()
@router.delete("/delete{todo_id}", status_code=status.HTTP_200_OK)
async def delete_admin(user: user_dependency, db:db_dependency, todo_id: int =Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Provided ID is not matched with data in db')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
