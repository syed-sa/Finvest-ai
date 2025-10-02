from fastapi import APIRouter, status
from fastapi_cache.decorator import cache  # type: ignore
from pydantic import BaseModel

from src.core.config import settings


router = APIRouter()

class HealthCheckResponse(BaseModel):
    status: str = "ok"


@router.get("/ping", tags=["health"], status_code=status.HTTP_200_OK)
@cache(expire=settings.CACHE_TTL)  # type: ignore
async def pong() -> HealthCheckResponse:
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    return HealthCheckResponse()
