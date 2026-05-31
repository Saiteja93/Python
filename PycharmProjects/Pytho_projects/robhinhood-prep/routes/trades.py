from fastapi import HTTPException, APIRouter, Depends
from typing import List, Annotated
from starlette import status
import uuid
from schemas import TradesCreate, TradeResponse
from models import TradeModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from kafka import KafkaProducer
import json

# ──────────────────────────────────────────────
# KAFKA SETUP
# ──────────────────────────────────────────────
KAFKA_TOPIC = "trade-events"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
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

# ──────────────────────────────────────────────
# GET all trades
# ──────────────────────────────────────────────
@router.get("/", response_model=List[TradeResponse], status_code=status.HTTP_200_OK)
async def get_all_trades(db: db_dependency):
    trades = db.query(TradeModel).all()
    if not trades:
        raise HTTPException(status_code=404, detail="No trades found")
    return trades

# ──────────────────────────────────────────────
# GET trade by ID
# ──────────────────────────────────────────────
@router.get("/id/{trade_id}", response_model=TradeResponse)
async def get_trade_id(trade_id: str, db: db_dependency):
    if not trade_id.strip():
        raise HTTPException(status_code=400, detail="trade_id cannot be empty")
    
    trade = db.query(TradeModel).filter(
        TradeModel.trade_id == trade_id
    ).first()

    if not trade:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    return trade

# ──────────────────────────────────────────────
# GET trades by symbol
# ──────────────────────────────────────────────
@router.get("/symbol/{symbol}", response_model=List[TradeResponse])
async def trades_symbol(symbol: str, db: db_dependency):
    if not symbol.strip():
        raise HTTPException(status_code=400, detail="symbol cannot be empty")
    
    if len(symbol) > 10:
        raise HTTPException(status_code=400, detail="Invalid symbol")

    trades = db.query(TradeModel).filter(
        TradeModel.symbol == symbol.upper()
    ).all()

    if not trades:
        raise HTTPException(status_code=404, detail=f"No trades found for {symbol.upper()}")
    
    return trades

# ──────────────────────────────────────────────
# GET portfolio value
# ──────────────────────────────────────────────
@router.get("/portfolio/value")
async def get_portfolio_value(db: db_dependency):
    total = db.query(func.sum(TradeModel.total_value)).scalar()
    total_value = total if total else 0.0
    return {
        "total_value": round(total_value, 2),
        "currency": "USD"
    }

# ──────────────────────────────────────────────
# POST — create trade (Kafka pattern)
# ──────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_trade(trade: TradesCreate):
    if trade.side not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")

    if trade.quantity <= 0:
        raise HTTPException(status_code=400, detail="quantity must be greater than 0")

    if trade.price <= 0:
        raise HTTPException(status_code=400, detail="price must be greater than 0")

    if not trade.symbol.strip():
        raise HTTPException(status_code=400, detail="symbol cannot be empty")

    trade_id = str(uuid.uuid4())

    trade_event = {
        "trade_id": trade_id,
        "symbol": trade.symbol.upper(),
        "side": trade.side,
        "quantity": trade.quantity,
        "price": float(trade.price),
        "total_value": trade.price * trade.quantity
    }

    producer.send(
        KAFKA_TOPIC,
        key=trade.symbol.upper(),
        value=trade_event
    )
    producer.flush()

    return {"status": "pending", "trade_id": trade_id}

# ──────────────────────────────────────────────
# DELETE trade
# ──────────────────────────────────────────────
@router.delete("/{trade_id}", status_code=status.HTTP_200_OK)
async def trade_delete(trade_id: str, db: db_dependency):
    if not trade_id.strip():
        raise HTTPException(status_code=400, detail="trade_id cannot be empty")

    trade = db.query(TradeModel).filter(
        TradeModel.trade_id == trade_id
    ).first()

    if not trade:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")

    db.delete(trade)
    db.commit()
    return {"message": f"Trade {trade_id} deleted successfully"}