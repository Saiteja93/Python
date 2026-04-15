from fastapi import FastAPI, Depends, HTTPException, Path,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from ..P_database import SessionLocal
from ..P_models import Todos
from .p_auth import get_current_user


router = APIRouter(
    prefix = "/todos",
    tags=['todos']
)


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
    description : str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def todo_filter(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0, description="ID must be greate than 0")):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No data found with that ID")

    return todo_model


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_data(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    todo_model = Todos(**todo_request.model_dump(), owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    return{"message":"Data created successfully"}


@router.put("/{todos_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_data(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest, todos_id: int= Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).filter(Todos.id == todos_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No data found with that ID")

    todo_model.title= todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
    return {"message":"Data updated successfully"}


@router.delete("{todo_id}")
async def delete_data(user: user_dependency, db:db_dependency, todo_id: int =Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No data found with that ID")

    db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully"}