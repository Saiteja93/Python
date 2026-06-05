from fastapi import HTTPException, APIRouter, Depends,Request, BackgroundTasks
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
from slowapi import Limiter
from slowapi.util import get_remote_address
import time as time_module
from app.logger import logger
import os
import time

load_dotenv()
limiter = Limiter(key_func=get_remote_address)
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
# Kafka Background task
# ──────────────────────────────────────────────
def send_to_kafka_background(trade_event: dict, db_session):
    
    start = time_module.time()

    kafka_success = False
    for attempt in range(3):
        try:
            producer = get_producer()
            producer.send(
                KAFKA_TOPIC,
                key=trade_event["symbol"],
                value=trade_event
            )
            producer.flush()
            kafka_success = True
            #print(f"Background: Trade sent to kafka:{trade_event['trade_id']}")
            logger.info("kafka_send_success",
                        trade_id = trade_event["trade_id"],
                        kafka_time_ms= kafka_time)
            
            break
        except Exception as e:
            #print(f"kafka retry{attempt + 1}/3...")
            logger.warning("kafka_retry",
                           trade_id = trade_event["trade_id"],
                           attempt= attempt + 1)
            time.sleep(1)
    
    #Fallback path to - DB directly        
    if not kafka_success:
        try:
            #print(f"Kafka down — falling back to DB")
            logger.error("kafka_failed_db_fallback",
                        trade_id = trade_event["trade_id"])
            
            new_trade = TradeModel(
                trade_id=trade_event['trade_id'],
                symbol=trade_event['symbol.upper'],
                side=trade_event['side'],
                price=float(trade_event['price']),
                quantity=trade_event['quantity'],
                total_value=round(trade_event['price'] * trade_event['quantity'], 2),
                user_id = trade_event["user_id"],
                username = trade_event["username"]
            )
            db_session.add(new_trade)
            db_session.commit()
            #print(f"Fallback DB save successful: {trade_event['trade_id']}")
            logger.info("db_fallback_success",
                        trade_id = trade_event["trade_id"])
            
        except Exception as db_error:
            db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Both Kafka and DB unavailable — please try again"
            )
        logger.error("kafka_and_db_failed",
                    trade_id=trade_event["trade_id"],
                    error=str(db_error))
        
    end = time_module.time()
    kafka_time = round((end-start) * 1000, 2)
    print(f"Kafka send time:{kafka_time}ms")



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
@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_trades(db: db_dependency, 
                        current_user: dict = Depends(get_current_user),
                        page: int=1,
                        limit: int=10):
    
    offset = (page -1) * limit
    try:
        total = db.query(TradeModel)\
            .filter(TradeModel.user_id == current_user["user_id"])\
            .count()
            
        trades = db.query(TradeModel)\
            .filter(TradeModel.user_id == current_user["user_id"])\
            .order_by(TradeModel.created_at.desc())\
            .offset(offset).limit(limit)\
            .all()
        
        if not trades:
           raise HTTPException(status_code=404, detail="No trades found")
        return {
            "trades": trades,
            "total": total,
            "page": page,
            "limit":limit,
            "pages": (total + limit -1)// limit 
        }
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
            #print(f"Cache HIT for {symbol}")
            logger.info("cache_hit", symbol=symbol)
            return json.loads(cached)
    except Exception:
        #print(f"Redis unavailable - falling back to DB")
        logger.warning("redis_unavailable", action="cache_read")
     
    try:    
        #print(f"Cache miss for {symbol} - querying DB")
        logger.info("cache_miss", symbol=symbol)

        trades = db.query(TradeModel).filter(
            TradeModel.symbol == symbol.upper()).all()

        if not trades:
            raise HTTPException(status_code=404, detail=f"No trades found for {symbol.upper()}")

        try:    
            #Stored in redis for 60seconds
            trades_data = [TradeResponse.model_validate(t).model_dump() for t in trades]
            redis_client.setex(cache_key, 60, json.dumps(trades_data))
            print(f"stored in cache:{cache_key}")
        except Exception:
            print(f"Redis unavilable - skipping cache store")

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
@limiter.limit("100/minute")
async def create_trade(request: Request,
                       trade: TradesCreate, 
                       db:db_dependency,
                       background_tasks: BackgroundTasks, 
                       current_user: dict = Depends(get_current_user)
                       ):
    start_time = time_module.time() #start timer
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
   
    #send to kafka in background
    background_tasks.add_task(send_to_kafka_background, trade_event, db)
    end_time = time_module.time() #End time

    response_time = round((end_time - start_time) * 1000, 2)
    print(f" Response time: {response_time}ms")

    #invalidate redis cache for this symbol
    cache_key = f"trades:symbol:{trade.symbol.upper()}"
    redis_client.delete(cache_key)
    #print(f"Cache invalidated for {trade.symbol.upper()}")
    logger.info("cache_invalidated",
            symbol= trade.symbol.upper())

    logger.info("trade_received",
                trade_id = trade_id,
                symbol=trade_event["symbol"],
                user_id=current_user["user_id"],
                response_time_ms=response_time
                )
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