from pydantic import BaseModel, Field, constr
from typing import Optional

class ChatRequest(BaseModel):
    user_message: constr(min_length=1) = Field(
        ...,
        description="The user's message. Cannot be empty."
    )
    sessionId: Optional[str] = Field(
        None,
        description="Optional session ID. Will be empty for first-time sessions."
    )