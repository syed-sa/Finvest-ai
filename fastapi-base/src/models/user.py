# User model
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, BigInteger, Boolean, Text, String
from src.models.base import BaseModel
from src.models.chat import ChatSession
from typing import List

class User(BaseModel, table=True):
    __tablename__ = "users"

    user_name: str = Field(sa_column=Column(String(255), nullable=False))
    email: Optional[str] = Field(default=None, sa_column=Column(String(255), unique=True, nullable=True))

    # Use List, not Optional[list]
    chat_sessions: List["ChatSession"] = Relationship(back_populates="user")