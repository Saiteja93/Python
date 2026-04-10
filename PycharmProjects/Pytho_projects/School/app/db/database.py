from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind = engine)
Base = declarative_base()