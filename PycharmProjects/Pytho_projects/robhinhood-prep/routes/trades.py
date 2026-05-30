from fastapi import FastAPI, HTTPException,APIRouter,Depends
from typing import Optional,List,Annotated
from starlette import status
import uuid
from schemas import TradesCreate,TradeResponse
from models import TradeModel
from sqlalchemy.orm import session
from sqlalchemy import func
from database import get_db
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v: json.dumps(v).encode("utf-8"),
    key_serializer = lambda k: k.encode("utf-8")
)

KAFKA_TOPIC = "trade-events"
router = APIRouter(
        prefix="/trades",
        tags=["Trades"]
)

#trades_db = {}


db_dependency = Annotated[session, Depends(get_db)]
#API Endpoints

#GET all trades
@router.get("/", response_model=List[TradeResponse],status_code=status.HTTP_200_OK)
async def get_all_trades(db: db_dependency):
    return db.query(TradeModel).all()

#GET trade by ID
@router.get("/id/{trade_id}",response_model=TradeResponse)
async def get_trade_id(trade_id: str, db:db_dependency):
    trade = db.query(TradeModel).filter(
        TradeModel.trade_id == trade_id
        ).first()

    if not trade:
        raise HTTPException(status_code=404, detail="No trade found in database")
    return trade


#GET trade by symbol
@router.get("/symbol/{symbol}",response_model=List[TradeResponse])
async def trades_symbol(symbol: str,db: db_dependency):
    return db.query(TradeModel).filter(
        TradeModel.symbol == symbol.upper()
        ).all()
    
#GET portfolio value
@router.get("/portfolio/value",)
async def get_portfolio_value(db:db_dependency):
    total = db.query(func.sum(TradeModel.total_value)).scalar()

    total_value = total if total else 0.0
    
    return {
        "total_value": round(total_value,2),
        "currency": "USD"
    }


#POST method to create trade
'''
@router.post("/",status_code=status.HTTP_201_CREATED) #response_model=TradeResponse,
async def create_trade(trade: TradesCreate): #db:db_dependency)

    if trade.side not in  ["buy","sell"]:
        raise HTTPException(status_code=400, detail="side must be buy or sell ")
    
    if trade.quantity <=0:
        raise HTTPException(status_code=400, detail="Quantity must be more than 0")
    

    new_trade = TradeModel(
        trade_id = str(uuid.uuid4()),
        symbol = trade.symbol.upper(),
        side = trade.side,
        price = trade.price,
        quantity = trade.quantity,
        total_value = trade.price * trade.quantity
    )


    trades_db[trade_id]=new_trade
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    trade_id = str(uuid.uuid4())
    trade_event = {
        "trade_id": trade_id,
        "symbol": trade.symbol,
        "side": trade.side,
        "quantity": trade.quantity,
        "price": float(trade.price),
        "total_value": trade.price * trade.quantity
    }

    producer.send(
        KAFKA_TOPIC,
        key=trade.symbol.encode("utf-8"),
        value=trade_event
    )

    producer.flush()

    return {"status":"pending", "trade_id": trade_id}

'''

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_trade(trade: TradesCreate):
    if trade.side not in ["buy","sell"]:
        raise HTTPException(status_code=400, detail="side must be buy or sell")
    
    if trade.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be more than 0")
    
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

#delete data
@router.delete("/{trade_id}",status_code=status.HTTP_200_OK)
async def trade_delete(trade_id: str,db:db_dependency):

    trade = db.query(TradeModel).filter(
        TradeModel.trade_id == trade_id
        ).first()

    if not trade:

        raise HTTPException(status_code=404, detail="No Trade found in database")
    
    
    db.delete(trade)
    db.commit()
    return {f"Deleted trade data of selecte{trade_id}"}



