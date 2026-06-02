from app.routes import trades
from fastapi import FastAPI
from app.database import engine,Base
from app.routes import auth


app= FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(trades.router)
app.include_router(auth.router)

@app.get("/health")
async def root():
    return {"status": "Trading API is online"}
