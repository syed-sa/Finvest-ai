from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from src.core.config import settings

router = APIRouter()


class HealthCheckResponse(JSONResponse):
    status: str = "ok"


@router.get(
    "/ping", tags=["health"], status_code=status.HTTP_200_OK, response_model=HealthCheckResponse
)
@cache(expire=settings.CACHE_TTL)  # type: ignore
def pong() -> HealthCheckResponse:
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    return HealthCheckResponse(content={"ping": "pong!"}, status_code=status.HTTP_200_OK)


# # Example route
# @router.get("/users", response_model=IGetResponseBase[list[UserRead]], tags=["users"])
# async def get_users(db=Depends(get_db)):
#     user_repo = UserRepository(db)

#     users = await user_repo.all()

#     return IGetResponseBase[list[User]](data=users)
