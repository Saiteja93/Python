
from fastapi import Depends, HTTPException, Path, Query,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from P_models import Todos
from P_database import SessionLocal, engine
from starlette import status
from pydantic import Field, BaseModel
from datetime import datetime
from .p_auth import get_current_user


router = APIRouter()

current_year = datetime.now().year

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    genre: str = Field(min_length=3)
    year_published: int = Field(ge=1800, le=current_year)
    is_available: bool
    rating: float = Field(ge=0, le=5)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return db.query(Todos).filter(Todos.owner_id  == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_by_id(user: user_dependency, db: db_dependency,todo_id : int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=401, detail='user is not authorized')

    todo_data = db.query(Todos).filter(todo_id == Todos.id ).filter(Todos.owner_id == user.get("id")).first()
    if todo_data is not None:
        return todo_data

    raise HTTPException(status_code=404, detail = "Id not found in data")


@router.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_data(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='user is not authorized')
    todo_data = Todos(**todo_request.model_dump(), owner_id = user.get("id"))
    db.add(todo_data)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_data(user: user_dependency, db: db_dependency, todo_request : TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='user is not authorized')

    todo_data = db.query(Todos).filter(todo_id == Todos.id ).filter(Todos.owner_id == user.get("id")).first()
    if todo_data is None:
        raise HTTPException(status_code=404, detail="No Id found matched with input")

    todo_data.title = todo_request.title
    todo_data.author = todo_request.author
    todo_data.genre = todo_request.genre
    todo_data.year_published = todo_request.year_published
    todo_data.is_available = todo_request.is_available
    todo_data.rating = todo_request.rating

    db.add(todo_data)
    db.commit()


@router.delete("/todo/todo_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(user: user_dependency, db: db_dependency,todo_id: int= Query(gt=0) ):
    if user is None:
        raise HTTPException(status_code=401, detail="User is not authorized")

    todo_data = db.query(Todos).filter(todo_id == Todos.id ).filter(Todos.owner_id == user.get("id")).first()

    if todo_data is None:
        raise HTTPException(status_code=404, detail= "Input ID is not found in data")

    db.query(Todos).filter(todo_id == Todos.id).delete()
    db.commit()

