from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, BigInteger, Boolean, Text, String
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import DateTime
from src.models.base import BaseModel
from src.models.user import User
from typing import List

# Session model


class ChatSession(BaseModel, table=True):
    __tablename__ = "chat_sessions"

    user_id: int = Field(foreign_key="users.id", nullable=False)
    title: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))

    user: Optional[User] = Relationship(back_populates="chat_sessions")
    messages: List["Message"] = Relationship(back_populates="session")


class Message(BaseModel, table=True):
    __tablename__ = "messages"

    session_id: int = Field(foreign_key="chat_sessions.id", nullable=False)
    user_message: str = Field(sa_column=Column(Text, nullable=False))
    ai_reply: str = Field(sa_column=Column(Text, nullable=False))

    session: Optional[ChatSession] = Relationship(back_populates="messages")
