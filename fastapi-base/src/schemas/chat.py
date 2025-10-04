from pydantic import BaseModel, Field, constr, field_validator
from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_message: constr(min_length=1) = Field(
        ..., description="The user's message. Cannot be empty."
    )
    session_id: Optional[str] = Field(
        None, description="Optional session ID. Will be empty for first-time sessions."
    )




class ChatSessionCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title of the chat session")
    user_id: int = Field(..., gt=0, description="ID of the user, must be positive")

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty or only whitespace")
        return v
    
class MessageCreate(BaseModel):
    session_id: int = Field(..., gt=0, description="ID of the chat session")
    user_message: str = Field(..., min_length=1, description="User's message")
    ai_reply: str = Field(..., description="AI's reply")
