from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from src.schemas.chat import ChatRequest
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import ObjectNotFound, UnAuthorized
from src.schemas.common import IResponseBase
from src.api.common import create_access_token
from src.core.config import settings
from fastapi import Request
from src.models.chat_session import ChatSession
from src.repositories.base import BaseSQLAlchemyRepository

router = APIRouter()

@router.post("/chat")
async def chat(request: Request, db: AsyncSession = Depends(get_db), title: Optional[str] = None):
    """
    Create a new chat session for the authenticated user.
    Everything is handled inside this function using the generic repository.
    """
    
    if not request.state.user_id:
        raise UnAuthorized("User not authenticated", "The user is not authenticated")

    user_id = request.state.user_id

   
    chat_repo = BaseSQLAlchemyRepository[ChatSession, ChatSession, None](ChatSession, db)

    
    session_data = ChatSession(user_id=user_id, title=title)

   
    new_session = await chat_repo.create(session_data)


    return {
        "status": "success",
        "session_id": new_session.id,
        "title": new_session.title
    }