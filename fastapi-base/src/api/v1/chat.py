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
from src.models.chat import ChatSession,Message
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from typing import List, Optional
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

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


from fastapi_pagination import Params, Page

@router.get("/sessions", response_model=Page[ChatSession])
async def get_chat_sessions(
    request: Request, 
    params: Params = Depends(),   # handles page & size params (?page=1&size=20)
    db: AsyncSession = Depends(get_db)
):
    """
    Get all chat sessions of the authenticated user with pagination.
    """
    if not request.state.user_id:
        raise UnAuthorized(
            "User not authenticated", 
            "The user is not authenticated"
        )

    user_id = request.state.user_id
    chat_repo = BaseSQLAlchemyRepository[ChatSession, ChatSession, None](ChatSession, db)

    # ✅ Use the repository's built-in paginate method
    sessions_page: Page[ChatSession] = await chat_repo.paginate(
        filters={"user_id": user_id},
        sort_field="created_at",
        sort_order="desc",
    )

    return sessions_page




@router.get("/sessions/{session_id}/messages")
async def get_chat_session_messages(
    session_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    cursor: Optional[str] = Query(None, description="Pagination cursor (created_at timestamp)"),
    limit: int = Query(20, description="Max number of messages to fetch"),
    direction: str = Query("next", regex="^(next|previous)$", description="Pagination direction"),
):
    """
    Get messages for a specific chat session, with cursor-based pagination.
    Works similar to how ChatGPT fetches conversation history.
    """
    if not request.state.user_id:
        raise UnAuthorized("User not authenticated", "The user is not authenticated")

    user_id = request.state.user_id

    # Ensure the chat session belongs to the authenticated user
    chat_repo = BaseSQLAlchemyRepository[ChatSession, ChatSession, None](ChatSession, db)
    session = await chat_repo.get(id=session_id, user_id=user_id)
    if not session:
        raise UnAuthorized("Forbidden", "Chat session not found or does not belong to the user")

    message_repo = BaseSQLAlchemyRepository[Message, Message, None](Message, db)

    # Use time-based pagination from BaseSQLAlchemyRepository
    cursor_dt = None
    if cursor:
        from datetime import datetime
        cursor_dt = datetime.fromisoformat(cursor)

    pagination = await message_repo.paginate_by_time(
        cursor=cursor_dt,
        limit=limit,
        direction=direction,
        time_field="created_at",
        sort_order="asc",  # messages in order of conversation
        filters={"session_id": session_id},
    )

    return {
        "status": "success",
        "session_id": session_id,
        "messages": [
            {
                "id": m.id,
                "user_message": m.user_message,
                "ai_reply": m.ai_reply,
                "created_at": m.created_at,
            }
            for m in pagination.items
        ],
        "pagination": {
            "has_next": pagination.has_next,
            "has_previous": pagination.has_previous,
            "next_cursor": pagination.next_cursor.isoformat() if pagination.next_cursor else None,
            "previous_cursor": pagination.previous_cursor.isoformat() if pagination.previous_cursor else None,
            "total_count": pagination.total_count,
        },
    }
