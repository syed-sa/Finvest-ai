from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse, Response

from src.api.v1 import health

# To include more routes go as
# from src.api.v1 import <module_name>
# then at the end of file api_router.include_router(<module_name>.router)


home_router = APIRouter()


@home_router.get("/", response_description="Homepage", include_in_schema=False)
def home() -> Response:
    return PlainTextResponse("127.0.0.1", status_code=status.HTTP_200_OK)


api_router = APIRouter()
api_router.include_router(health.router)
