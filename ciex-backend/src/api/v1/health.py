from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

router = APIRouter()


@router.get("/ping", tags=["health"])
def pong() -> Response:
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    return JSONResponse({"ping": "pong!"})


# # Example route
# @router.get("/users", response_model=IGetResponseBase[list[UserRead]], tags=["users"])
# async def get_users(db=Depends(get_db)):
#     user_repo = UserRepository(db)

#     users = await user_repo.all()

#     return IGetResponseBase[list[User]](data=users)
