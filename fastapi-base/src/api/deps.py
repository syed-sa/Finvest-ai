from typing import AsyncGenerator, cast

from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.session import get_session


def get_redis_url() -> str:
    return settings.REDIS_URL or ""


async def get_redis_client() -> Redis:
    redis = Redis.from_url(
        get_redis_url(),
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    await redis.ping()  # ensure connection
    return cast(Redis, redis)  # type: ignore


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    """
    async for session in get_session():
        yield session
