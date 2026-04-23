from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.ai import get_property_agent
from app.core.db import get_db
from app.ai.agent import PropertyAgent
from app.modules.conversations.service import ConversationService
from .service import AssistantService
from .schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(
    request: ChatRequest,
    db: Session = Depends(get_db),
    property_agent: PropertyAgent = Depends(get_property_agent),
):
    """Process user chat input with context-aware property recommendations.
    
    This endpoint:
    1. Retrieves conversation history from database
    2. Merges with request history for RAG context
    3. Generates AI recommendations using OpenRouter
    4. Returns recommendations and filters
    """
    # Retrieve existing conversation history from database
    conversation = ConversationService.get_or_create_conversation(
        db, request.session_id
    )
    
    # Build complete history: DB messages + request history
    db_messages = [
        {"role": msg.role, "content": msg.content} for msg in conversation.messages
    ]
    complete_history = db_messages + request.history
    
    # Update request with complete history for RAG context
    request.history = complete_history
    
    # Process chat with agent and service
    result = AssistantService.process_chat(db, request, property_agent)
    
    return ChatResponse(
        success=True,
        message="Chat processed successfully",
        data=result,
    )
