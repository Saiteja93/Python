from sqlalchemy import Column,Integer,String,Boolean

from api.practice_TODOAPP.P_database import Base


class Todos(Base):
    __tablename__= 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default = False)




