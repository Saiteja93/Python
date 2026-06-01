from pydantic import BaseModel,Field

#DataModel pydantic
class TradesCreate(BaseModel):
    symbol: str
    price: float = Field(gt=0)
    quantity: int=Field(gt=0)
    side: str

class TradeResponse(BaseModel):
    trade_id: str
    symbol: str
    price: float
    quantity: int
    side: str
    total_value: float

    class Config:
        from_attributes= True
