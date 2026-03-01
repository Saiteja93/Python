
from fastapi import FastAPI
import P_models

from P_database import  engine

from routers import p_auth,p_todos,p_admin



app = FastAPI()

P_models.Base.metadata.create_all(bind=engine)
app.include_router(p_auth.router)
app.include_router(p_todos.router)
app.include_router(p_admin.router)


