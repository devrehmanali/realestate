from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from .service import AssistantService
from .schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest, db: Session = Depends(get_db)):
    return AssistantService.process_chat(db, request)
