from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from src.schemas.chat import ChatRequest, ChatSessionCreate, MessageCreate
from src.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.core.exceptions import ObjectNotFound, UnAuthorized
from src.schemas.common import IResponseBase
from src.schemas.chat import ChatRequest
from src.api.common import create_access_token
from src.core.config import settings
from fastapi import Request, Query
from src.models.chat import ChatSession, Message
from src.agent.agentRout import AgentRouter, handleLLMResponseText
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.agent.cloudLLM import mcp_gateway,cloud_llm

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    session_id: int = Query(None),
):
    """
    Create a new chat session for the authenticated user.
    Everything is handled inside this function using the generic repository.
    """
    user_id = request.state.user_id
    new_session = None

    
    # If no session_id is provided, create a new session
    if not session_id:
        chat_repo = BaseSQLAlchemyRepository[ChatSession, ChatSessionCreate, None](
            ChatSession, db
        )
        title = " ".join(body.user_message.split()[:3])
        session_data = ChatSession(user_id=user_id, title=title)

        new_session = await chat_repo.create(session_data)
        session_id = new_session.id

    # Create message entry
    message = Message(
        user_message=body.user_message,
        session_id=session_id,
        ai_reply="",
    )
    message_repo = BaseSQLAlchemyRepository[Message, MessageCreate, None](Message, db)
    await message_repo.create(message)
    # Explicit commit (optional, already done by db.begin())
    # Call LLM / MCPTool outside transaction if needed
    text = await AgentRouter(body.user_message)
    action = handleLLMResponseText(text)

    if action == "MCPTool":
        result =  mcp_gateway(body.user_message, session_id=session_id)
    else:
        result =  cloud_llm(body.user_message, session_id=session_id)

    # Prepare response message
    message_text = "Chat session created successfully."

    return IResponseBase[dict](
        message=message_text,
        data={
            "session_id": session_id,
            "title": new_session.title if new_session else None,
            "action_result": result,
            "action":action
        },
    )
