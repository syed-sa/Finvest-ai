from datetime import datetime
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    """Base model with common fields for all tables"""
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
