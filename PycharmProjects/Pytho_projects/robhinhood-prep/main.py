from routes import trades
from fastapi import FastAPI
from database import engine,Base


app= FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(trades.router)

@app.get("/health")
async def root():
    return {"status": "Trading API is online"}
