# User model
from typing import Optional

from sqlmodel import (
    Column,
    Field,
    String,
)


from src.models.base import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "user"
    
    user_name: str = Field(min_length=1)
    email: str | None = Field(default=None, unique=True, regex=r'^[^@]+@[^@]+\.[^@]+$')
    hashed_password: str = Field(min_length=1)

