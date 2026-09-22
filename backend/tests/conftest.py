import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


# Test database engine
test_engine = create_engine(
    settings.TEST_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all tables in the test database
    Base.metadata.create_all(bind=test_engine)

    yield

    # # Remove all tables after the complete test session
    # Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()