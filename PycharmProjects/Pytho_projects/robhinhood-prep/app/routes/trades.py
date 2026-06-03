from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Annotated
from starlette import status
import uuid
from app.schemas import TradesCreate, TradeResponse
from app.models import TradeModel, Users
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from kafka import KafkaProducer
import json
from app.redis_client import redis_client
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
import time

load_dotenv()

# ──────────────────────────────────────────────
# KAFKA SETUP
# ──────────────────────────────────────────────
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC","trade-events")

def get_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8")
        )

# ──────────────────────────────────────────────
# ROUTER SETUP
# ──────────────────────────────────────────────
router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

# ──────────────────────────────────────────────
# Current user
# ──────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("user_id")
        username = payload.get("username")
        role = payload.get("role")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {"user_id": user_id, "username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ──────────────────────────────────────────────
# GET all trades
# ──────────────────────────────────────────────
@router.get("/", response_model=List[TradeResponse], status_code=status.HTTP_200_OK)
async def get_all_trades(db: db_dependency, current_user : dict = Depends(get_current_user)):

    if current_user["role"]!= "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        trades = db.query(TradeModel).all()
        if not trades:
            raise HTTPException(status_code=404, detail="No trades found")
        return trades
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error:{str(e)}")

# ──────────────────────────────────────────────
# GET my trades
# ──────────────────────────────────────────────
@router.get("/my", response_model=List[TradeResponse], status_code=status.HTTP_200_OK)
async def get_my_trades(db: db_dependency, current_user: dict = Depends(get_current_user)):
    

    try:
        trades = db.query(TradeModel).filter(
            TradeModel.user_id == current_user["user_id"]
            ).all()
        
        if not trades:
           raise HTTPException(status_code=404, detail="No trades found")
        return trades
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    

# ──────────────────────────────────────────────
# GET trade by ID
# ──────────────────────────────────────────────
@router.get("/id/{trade_id}", response_model=TradeResponse)
async def get_trade_id(trade_id: str, db: db_dependency,
                       current_user: dict = Depends(get_current_user)):
    if not trade_id.strip():
        raise HTTPException(status_code=400, detail="trade_id cannot be empty")
    try: 
        trade = db.query(TradeModel).filter(
            TradeModel.trade_id == trade_id
            ).first()
        if not trade:
            raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
        if current_user["role"]!= "admin" and trade.user_id != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return trade
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

   

# ──────────────────────────────────────────────
# GET trades by symbol
# ──────────────────────────────────────────────
@router.get("/symbol/{symbol}", response_model=List[TradeResponse])
async def trades_symbol(symbol: str, db: db_dependency):
    if not symbol.strip():
        raise HTTPException(status_code=400, detail="symbol cannot be empty")
    
    if len(symbol) > 10:
        raise HTTPException(status_code=400, detail="Invalid symbol")
    
    symbol = symbol.upper()
    cache_key = f"trades:symbol:{symbol}"
    try:
        #Redis cache
        cached = redis_client.get(cache_key)
        if cached:
            print(f"Cache HIT for {symbol}")
            return json.loads(cached)
        
        print(f"Cache miss for {symbol} - querying DB")

        trades = db.query(TradeModel).filter(
            TradeModel.symbol == symbol.upper()).all()

        if not trades:
            raise HTTPException(status_code=404, detail=f"No trades found for {symbol.upper()}")
        
        #Stored in redis for 60seconds
        trades_data = [TradeResponse.model_validate(t).model_dump() for t in trades]
        redis_client.setex(cache_key, 60, json.dumps(trades_data))
        print(f"stored in cache:{cache_key}")
        return trades
    

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ──────────────────────────────────────────────
# GET portfolio value
# ──────────────────────────────────────────────
@router.get("/portfolio/value")
async def get_portfolio_value(db: db_dependency):
    try:
        total = db.query(func.sum(TradeModel.total_value)).scalar()
        total_value = total if total else 0.0
        return {
            "total_value": round(total_value, 2),
            "currency": "USD"
        }
    except HTTPException:
        raise
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ──────────────────────────────────────────────
# POST — create trade (Kafka pattern)
# ──────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_trade(trade: TradesCreate, 
                       db:db_dependency, 
                       current_user: dict = Depends(get_current_user)
                       ):
    db_user = db.query(Users).filter(Users.id==current_user["user_id"]).first()
    full_name = f"{db_user.first_name} {db_user.last_name}" if db_user else current_user["username"]
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    producer = get_producer()
    if trade.side not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")

    if trade.quantity <= 0:
        raise HTTPException(status_code=400, detail="quantity must be greater than 0")

    if trade.price <= 0:
        raise HTTPException(status_code=400, detail="price must be greater than 0")

    if not trade.symbol.strip():
        raise HTTPException(status_code=400, detail="symbol cannot be empty")

    trade_id = str(uuid.uuid4())
    # check for duplicate request
    idempotency_key = f"idempotency:{trade_id}"
    if redis_client.get(idempotency_key):
        return {"status":"duplicate","trade_id":trade_id}
    
    #mark as processed for 60 seconds
    redis_client.setex(idempotency_key,60,"processed")

    trade_event = {
        "trade_id": trade_id,
        "symbol": trade.symbol.upper(),
        "side": trade.side,
        "quantity": trade.quantity,
        "price": float(trade.price),
        "total_value": round(trade.price * trade.quantity, 2),
        "user_id": current_user["user_id"],
        "username": current_user["username"]
    }
    kafka_success = False
    for attempt in range(3):

        try:
            producer.send(
                KAFKA_TOPIC,
                key=trade.symbol.upper(),
                value=trade_event
            )
            producer.flush()
            kafka_success = True
            print(f"Trade sent to kafka:{trade_id}")
            break
        except Exception as e:
            print(f"kafka retry{attempt + 1}/3...")
            time.sleep(1)
    
    #Fallback path to - DB directly        
    if not kafka_success:
        try:
            print(f"Kafka down — falling back to DB")
            new_trade = TradeModel(
                trade_id=trade_id,
                symbol=trade.symbol.upper(),
                side=trade.side,
                price=float(trade.price),
                quantity=trade.quantity,
                total_value=round(trade.price * trade.quantity, 2),
                user_id = current_user["user_id"],
                username = current_user["username"]
            )
            db.add(new_trade)
            db.commit()
            print(f"Fallback DB save successful: {trade_id}")
        except Exception as db_error:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Both Kafka and DB unavailable — please try again"
            )

    
    #invalidate redis cache for this symbol
    cache_key = f"trades:symbol:{trade.symbol.upper()}"
    redis_client.delete(cache_key)
    print(f"Cache invalidated for {trade.symbol.upper()}")


    return {"status": "pending", "trade_id": trade_id, "placed_by": full_name}

# ──────────────────────────────────────────────
# DELETE trade
# ──────────────────────────────────────────────
@router.delete("/{trade_id}", status_code=status.HTTP_200_OK)
async def trade_delete(trade_id: str, db: db_dependency):
    if not trade_id.strip():
        raise HTTPException(status_code=400, detail="trade_id cannot be empty")
    try:

        trade = db.query(TradeModel).filter(
            TradeModel.trade_id == trade_id
        ).first()

        if not trade:
            raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")

        db.delete(trade)
        db.commit()
        return {"message": f"Trade {trade_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")