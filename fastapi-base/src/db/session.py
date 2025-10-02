from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings


async_engine = create_async_engine(
    settings.POSTGRES_URL,  # type: ignore
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def add_postgresql_extension() -> None:
    async with AsyncSessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await db.execute(query)
        await db.commit()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
