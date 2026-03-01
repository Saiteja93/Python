from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



#for sqlite
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread' : False})

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test123!@localhost/TodoApplicationDatabase'
#engine = create_engine(SQLALCHEMY_DATABASE_URL)


#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test123!@127.0.0.1:3306/TodoApplicationDatabase'
#engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()