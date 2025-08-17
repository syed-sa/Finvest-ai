from typing import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from src.core.config import settings


test_engine = create_engine(
    settings.POSTGRES_URL,  # Consider using a TEST_POSTGRES_URL instead
    echo=settings.DEBUG,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def add_postgresql_extension_test() -> None:
    with TestSessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        db.execute(query)
        db.commit()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Create a test database session with proper cleanup.
    Each test gets a fresh transaction that's rolled back after the test.
    """

    add_postgresql_extension_test()

    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def setup_test_db(db_session):
    """Create tables for testing"""

    # Create tables in the test database
    SQLModel.metadata.create_all(bind=db_session.bind)
    yield
    # Cleanup is handled by the db_session fixture rollback
