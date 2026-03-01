
from sqlalchemy import create_engine, StaticPool,text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..models import Todos,Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username":"codewithsai", "id":1, "user_role": "admin"}

client = TestClient(app)
@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code",
        description = "need to learn daily",
        priority = 5,
        complete = False,
        owner_id = 1

    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = "codewithsai",
        email = "codewithsai@gmail.com",
        first_name = "sai",
        last_name = "teja",
        hashed_password = bcrypt_context.hash("test123"),
        role = "admin",
        phone_number = 1234567899

    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
