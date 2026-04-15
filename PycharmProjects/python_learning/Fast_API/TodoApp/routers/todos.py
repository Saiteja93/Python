from typing import Annotated


from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Request,status
from starlette import status
from starlette.templating import Jinja2Templates

from models import Todos
from database import SessionLocal
from pydantic import BaseModel,Field

from .auth import get_current_user, redirect_to_login
from starlette.responses import RedirectResponse


router = APIRouter(prefix="/todos", tags=['todos'])

templates = Jinja2Templates(directory="Templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str=Field(min_length=3, max_length=150)
    priority : int=Field(gt=0,lt=6)
    complete : bool






###pages###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get('access_token')
        user =  await get_current_user(token)
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse("todos.html",{

            "request": request,
            "todos": todos,
            "user": user
        })

    except Exception as e:
        # Log the error to your terminal so you can see what went wrong
        print(f"Redirecting to login due to error: {e}")
        return redirect_to_login()



@router.get('/add-todo')
async def render_todo_page(request: Request):
    try:
        token = request.cookies.get('access_token')
        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse('add-todo.html', {"request": request, "user": user})
    except:
        return redirect_to_login()

@router.get('/edit-todo/{todo_id}')
async def render_edit_todo(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "user":user, "todo":todo})
    except:
        return redirect_to_login()
###Endpoints###


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency ):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_id(user: user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('id')).first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo is not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest,
                      user: user_dependency,
                      db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo( user: user_dependency,
                      db: db_dependency,
                       todo_request: TodoRequest,
                      todo_id: int=Path(gt=0),
                      ):
    if user is None:
        raise HTTPException(status_code=401, detail="No Id found in data")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No Id found in data")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency,
                      todo_id : int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404, detail="Id not found to delete")

    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('id')).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Id not found to delete")

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()


