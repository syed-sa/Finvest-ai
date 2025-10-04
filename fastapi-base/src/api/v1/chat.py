from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from src.schemas.chat import ChatRequest, ChatSessionCreate
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import ObjectNotFound, UnAuthorized
from src.schemas.common import IResponseBase
from src.schemas.chat import ChatRequest
from src.api.common import create_access_token
from src.core.config import settings
from fastapi import Request
from src.models.chat import ChatSession
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(
    body: ChatRequest,  # ✅ request body comes here
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new chat session for the authenticated user.
    Everything is handled inside this function using the generic repository.
    """
    user_id = request.state.user_id 
    chat_repo = BaseSQLAlchemyRepository[ChatSession, ChatSessionCreate, None](ChatSession, db)
    #handle session id logic
    title = " ".join(body.user_message.split()[:3])
    session_data = ChatSession(user_id=user_id, title=title)

    new_session = await chat_repo.create(session_data)

    return IResponseBase[dict](
        message="Chat session created successfully",
        data={"session_id": new_session.id, "title": new_session.title},
    ) # to be changed