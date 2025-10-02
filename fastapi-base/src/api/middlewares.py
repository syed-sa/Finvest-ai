import logging
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import BaseModel
from src.core.exceptions import *

# Pydantic models
# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security scheme
security = HTTPBearer()

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list[str] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/login",
            "/register",
            "/health",
        ]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip authentication for excluded paths
        if self._should_skip_auth(request):
            return await call_next(request)
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnAuthorized("Auth header missing", "The HTTP auth header is missing")
        token = auth_header.split("Bearer ")[1]

        # Verify and decode the JWT token
        payload = self._verify_token(token)

        # Add user info to request state for use in endpoints
        request.state.user_id = payload.get("user_id")
        request.state.username = payload.get("username")
        request.state.token_data = payload
        logger.info(f"User {request.state.user_id} authenticated")
        response = await call_next(request)
        return response

    def _should_skip_auth(self, request: Request) -> bool:
        """Check if the request path should skip authentication"""
        path = request.url.path
        return any(exclude_path in path for exclude_path in self.exclude_paths)

    def _verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Check if token has expired
            exp = payload.get("exp")
            if exp and datetime.now().timestamp() > exp:
                raise UnAuthorized(
                    message="Token has expired", detail="The user session has expired"
                )
            return payload

        except jwt.ExpiredSignatureError:
            raise UnAuthorized(message="Token signature wrong", detail="JWT token invalid")

        except jwt.InvalidTokenError as exc:
            raise UnAuthorized(
                message="Token is not in expected format", detail="JWT Token not valid"
            )


class GlobalExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseBackendException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"message": exc.message, "detail": exc.detail, "status": exc.status},
            )
        except Exception as exc:
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "message": "Internal Server Error",
                    "detail": "An unexpected error occurred. Please try again later.",
                },
            )
