from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from src.schemas.auth import LoginRequest, SignupRequest
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import ObjectNotFound, UnAuthorized
from src.schemas.common import IResponseBase
from src.api.common import create_access_token
from src.core.config import settings
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_repo = BaseSQLAlchemyRepository[User, LoginRequest, SignupRequest](User, db)
    user = await user_repo.get(email=request.email)  # need to hash
    if not user:
        raise ObjectNotFound(f"User with email {request.email} not found", "Email does not exist")

    if user.hashed_password != request.password:
        raise UnAuthorized("Password is incorrect", "Password is wrong")

    access_token = create_access_token({"user_id": user.id, "username": user.user_name})
    refresh_token = create_access_token(
        {}, expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    )
    # Implement login logic here (authenticate and return token)
    return IResponseBase[dict](
        message="Login successful",
        data={"access_token": access_token, "refresh_token": refresh_token},
    )


@router.post("/signup")
async def signup(request: SignupRequest):
    # Implement signup logic here (create user in DB)
    return {"message": "Signup endpoint", "username": request.username}


@router.get("/validate")
async def get_current_user(request: Request):
    """
    Dependency to extract user info from JWTAuthMiddleware.
    Returns only status and username.
    """
    if not request or not request.state.username:
        raise UnAuthorized("User not authenticated", "The user is not authenticated")

    return IResponseBase[dict](
        status=True,
        data={"username": request.state.username},
    )
