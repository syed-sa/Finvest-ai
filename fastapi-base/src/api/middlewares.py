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


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list[str] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/auth/login",
            "/auth/register",
            "/health",
            "/",
        ]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip authentication for excluded paths
        if self._should_skip_auth(request):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return self._unauthorized_response("Missing or invalid authorization header")

        token = auth_header.split("Bearer ")[1]

        try:
            # Verify and decode the JWT token
            payload = self._verify_token(token)

            # Add user info to request state for use in endpoints
            request.state.user_id = payload.get("user_id")
            request.state.username = payload.get("sub")
            request.state.token_data = payload

        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception:
            return self._unauthorized_response("Invalid token")

        response = await call_next(request)
        return response

    def _should_skip_auth(self, request: Request) -> bool:
        """Check if the request path should skip authentication"""
        path = request.url.path
        return any(path.startswith(exclude_path) for exclude_path in self.exclude_paths)

    def _verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Check if token has expired
            exp = payload.get("exp")
            if exp and datetime.now(datetime.timezone.utc).timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
                )

            # Validate required fields
            if not payload.get("sub"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing subject",
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    def _unauthorized_response(self, detail: str) -> JSONResponse:
        """Return standardized unauthorized response"""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": detail},
            headers={"WWW-Authenticate": "Bearer"},
        )


class GlobalExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ObjectNotFound as exc:
            return JSONResponse(
                status_code=404,
                content={"error": "Not Found", "message": str(exc) or "Resource not found"},
            )
        except RepositoryError as exc:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Repository Error",
                    "message": str(exc) or "Repository operation failed",
                },
            )
        except BaseBackendException as exc:
            # Catch other backend exceptions if any
            return JSONResponse(
                status_code=400,
                content={"error": "Backend Error", "message": str(exc) or "Backend error occurred"},
            )
        except Exception as exc:
            # For unhandled exceptions
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later." + str(exc),
                },
            )


# JWT utility functions


# def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
#     """Extract user data from JWT token (for dependency injection)"""
#     try:
#         payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         user_id: int = payload.get("user_id")

#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials"
#             )

#         return TokenData(username=username, user_id=user_id)

#     except jwt.PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials"
#         )
