from fastapi import APIRouter, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel

from src.core.config import settings


router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: str = "ok"


@router.get("/ping", tags=["health"], status_code=status.HTTP_200_OK)
@cache(expire=settings.CACHE_TTL)  # type: ignore
def pong() -> HealthCheckResponse:
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    return HealthCheckResponse()


# # Example route
# @router.get("/users", response_model=IGetResponseBase[list[UserRead]], tags=["users"])
# async def get_users(db=Depends(get_db)):
#     user_repo = UserRepository(db)

#     users = await user_repo.all()

#     return IGetResponseBase[list[User]](data=users)
