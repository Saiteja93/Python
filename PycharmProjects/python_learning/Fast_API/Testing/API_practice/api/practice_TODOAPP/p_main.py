import os.path

from fastapi import FastAPI,Request
from api.practice_TODOAPP import P_models
from  api.practice_TODOAPP.P_database import engine
from api.practice_TODOAPP.routers import p_todos, p_auth,p_admin,p_users
from fastapi.templating import Jinja2Templates

app = FastAPI()

P_models.Base.metadata.create_all(bind=engine)
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir,"templates"))

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.include_router(p_todos.router)
app.include_router(p_auth.router)
app.include_router(p_admin.router)
app.include_router(p_users.router)