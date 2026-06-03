from app.routes import trades
from fastapi import FastAPI
from app.database import engine,Base
from app.routes import auth
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


app= FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

app.include_router(trades.router)
app.include_router(auth.router)

@app.get("/health")
async def root():
    return {"status": "Trading API is online"}
