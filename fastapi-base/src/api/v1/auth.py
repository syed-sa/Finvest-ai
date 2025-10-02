from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.schemas.auth import LoginRequest, SignupRequest
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import ObjectNotFound, RepositoryError, UnAuthorized
from src.schemas.common import IResponseBase
from src.api.common import create_access_token
from src.core.config import settings
from src.core.security import get_password_hash

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

@router.post("/signup", response_model=IResponseBase[dict])
async def signup(
    request: SignupRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    user_repo = BaseSQLAlchemyRepository[User, LoginRequest, SignupRequest](User, db)
    
    try:
        existing_email = await user_repo.get_by_email(request.email, raise_if_not_found=False)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        existing_username = await user_repo.get_by_username(request.username, raise_if_not_found=False)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash password before creating user
        hashed_password = get_password_hash(request.password)
        
        # Create user data with hashed password
        user_data = {
            "user_name": request.username,
            "email": request.email,
            "hashed_password": hashed_password
        }
        
        # Create the user
        user = await user_repo.create(user_data)
        
        # Create tokens
        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_access_token({}, expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
        
        return IResponseBase[dict](
            message="User created successfully",
            data={
                "user_id": user.id,
                "username": user.user_name,
                "email": user.email,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise RepositoryError(f"Error creating user: {str(e)}")
