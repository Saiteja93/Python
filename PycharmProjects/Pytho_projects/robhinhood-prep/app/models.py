from sqlalchemy import Column,Integer,Float,DateTime,String,Boolean,Numeric,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

#creating table for database
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True,nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
    trades = relationship("TradeModel", back_populates="user")




class TradeModel(Base):
    __tablename__ = "trades"
    trade_id = Column(String, primary_key=True,index=True)
    symbol = Column(String, nullable=False, index= True)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    side = Column(String, nullable=False,index=True)
    total_value = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    username = Column(String, nullable=True)
    user = relationship("Users", back_populates="trades")
