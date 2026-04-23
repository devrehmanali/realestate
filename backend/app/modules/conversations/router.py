from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from .service import ConversationService
from .schemas import ConversationResponse

router = APIRouter()

@router.get("/{session_id}", response_model=ConversationResponse)
def get_conversation_history(session_id: str, db: Session = Depends(get_db)):
    return ConversationService.get_or_create_conversation(db, session_id)
