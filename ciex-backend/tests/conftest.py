from typing import AsyncGenerator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from src.core.config import settings


async_test_engine = create_async_engine(
    settings.POSTGRES_URL,  # type: ignore
    echo=settings.DEBUG,
)
AsyncTestSessionLocal = async_sessionmaker(
    bind=async_test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def add_postgresql_extension_test() -> None:
    async with AsyncTestSessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await db.execute(query)
        await db.commit()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session with proper cleanup.
    Each test gets a fresh transaction that's rolled back after the test.
    """

    await add_postgresql_extension_test()

    async with async_test_engine.begin() as connection:
        session = AsyncTestSessionLocal(bind=connection)

        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
async def setup_test_db(db_session):
    """Create tables for testing"""

    # Create tables in the test database
    async with async_test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup is handled by the db_session fixture rollback
