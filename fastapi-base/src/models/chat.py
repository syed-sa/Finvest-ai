from datetime import datetime
from pydantic import Field as PydanticField
from sqlmodel import SQLModel, Field

from src.models.base import BaseModel

# # Session model


class ChatSession(BaseModel, table=True):
    __tablename__ = "chat_session"

    user_id: int = Field(foreign_key="user.id")
    title: str | None = Field(default=None, max_length=255)


class Message(BaseModel, table=True):
    __tablename__ = "message"

    session_id: int = Field(foreign_key="chat_session.id")
    user_message: str = Field(min_length=1)
    ai_reply: str = Field()
