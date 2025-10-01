from datetime import datetime
from typing import List, Optional

from sqlmodel import (
    Boolean,
    Column,
    Field,
    Relationship,
    String,
    Text,
)

from src.models.base import BaseModel

# Session model


class ChatSession(BaseModel, table=True):
    __tablename__ = "chat_sessions"

    user_id: int = Field(foreign_key="users.id", nullable=False)
    title: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))



class Message(BaseModel, table=True):
    __tablename__ = "messages"

    session_id: int = Field(foreign_key="chat_sessions.id", nullable=False)
    user_message: str = Field(sa_column=Column(Text, nullable=False))
    ai_reply: str = Field(sa_column=Column(Text, nullable=False))

