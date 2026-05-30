from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://admin:secret@127.0.0.1:5433/brokerage"
#DATABASE_URL = "postgresql://postgres:secret@localhost:5432/brokerage"

engine= create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()