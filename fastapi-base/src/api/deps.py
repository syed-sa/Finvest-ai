from typing import AsyncGenerator

import redis.asyncio as Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.session import get_session


def get_redis_url() -> str:
    return settings.REDIS_URL or ""


async def get_redis_client() -> Redis.Redis:
    redis = await Redis.from_url(
        get_redis_url(),
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    """
    async for session in get_session():
        yield session
