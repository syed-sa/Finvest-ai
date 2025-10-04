from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from src.schemas.auth import LoginRequest, SignupRequest
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import Conflict, ObjectNotFound, RepositoryError, UnAuthorized
from src.schemas.common import IResponseBase
from src.api.common import create_access_token
from src.core.config import settings
from src.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_repo = BaseSQLAlchemyRepository[User, LoginRequest, SignupRequest](User, db)
    user = await user_repo.get(email=request.email)
    if not user:
        raise ObjectNotFound(f"User with email {request.email} not found", "Email does not exist")

    # Verify password using hashing
    if not verify_password(request.password, user.hashed_password):
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


@router.post("/signup", response_model=IResponseBase[None])
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    """
    Register a new user
    """
    user_repo = BaseSQLAlchemyRepository[User, LoginRequest, SignupRequest](User, db)

    # Check if email is already registered
    if await user_repo.get(email=request.email, raise_if_not_found=False):
        raise Conflict(message="Email already registered")

    # Hash password
    hashed_password = hash_password(request.password)

    # Prepare user data
    user_data = {
        "user_name": request.username,
        "email": request.email,
        "hashed_password": hashed_password,
    }

    # Create user
    await user_repo.create_from_dict(user_data)

    # Return message only
    return IResponseBase[None](message="User created successfully", data=None)
