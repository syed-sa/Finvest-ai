from pydantic import BaseModel, EmailStr, Field, constr
from typing import Annotated


class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(description="Valid email address")]
    password: Annotated[
        constr(min_length=8, max_length=128),
        Field(description="Password must be between 8–128 characters"),
    ]


class SignupRequest(BaseModel):
    username: Annotated[
        constr(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$"),
        Field(description="3–30 chars, only letters, numbers, underscores"),
    ]
    email: Annotated[EmailStr, Field(description="Valid email address")]
    password: Annotated[
        constr(min_length=8, max_length=128),
        Field(description="Password must be between 8–128 characters"),
    ]
