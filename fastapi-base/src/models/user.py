# User model
from typing import List, Optional
from xmlrpc.client import Boolean

from sqlmodel import (
    Column,
    Field,
    Relationship,
    String,
)


from src.models.base import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "users"

    user_name: str = Field(sa_column=Column(String(255), nullable=False))
    email: Optional[str] = Field(
        default=None, sa_column=Column(String(255), unique=True, nullable=True)
    )
    
    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))

    is_active: bool = Field(default=True)

    # Use List, not Optional[list]
