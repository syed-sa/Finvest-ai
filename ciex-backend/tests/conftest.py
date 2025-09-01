from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from src.core.config import settings


# Create test engine with NullPool to avoid connection conflicts
async_test_engine = create_async_engine(
    settings.POSTGRES_URL,  # type: ignore
    echo=settings.DEBUG,
    poolclass=NullPool,  # Disable connection pooling for tests
)

AsyncTestSessionLocal = async_sessionmaker(
    bind=async_test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,  # Prevent automatic flushing
)


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Setup database schema once per test session"""
    async with async_test_engine.begin() as connection:
        # Add PostgreSQL extension
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        # Create all tables
        await connection.run_sync(SQLModel.metadata.create_all)

    yield

    # Cleanup: drop all tables after tests
    async with async_test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)

    await async_test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session with proper cleanup.
    Each test gets a fresh session with transaction rollback.
    """
    connection = await async_test_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection, expire_on_commit=False, autoflush=False, autocommit=False
    )

    try:
        yield session
        # Don't rollback here - let the test complete first
    except Exception:
        # await transaction.rollback()
        raise
    finally:
        await session.close()
        # Only rollback if transaction is still active and no exception occurred
        if transaction.is_active:
            await transaction.rollback()
        await connection.close()


# Configure pytest-asyncio
pytest_asyncio.fixture(scope="session", autouse=True)


async def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
