from fastapi import FastAPI
from api.practice_TODOAPP import P_models
from  api.practice_TODOAPP.P_database import engine
from api.practice_TODOAPP.routers import p_todos, p_auth
app = FastAPI()

P_models.Base.metadata.create_all(bind=engine)

app.include_router(p_todos.router)
app.include_router(p_auth.router)
