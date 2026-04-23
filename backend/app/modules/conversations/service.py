from sqlalchemy.orm import Session
from .models import Conversation, Message
from .schemas import ConversationCreate, MessageCreate
from typing import Optional

class ConversationService:
    @staticmethod
    def get_or_create_conversation(db: Session, session_id: str) -> Conversation:
        conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
        if not conversation:
            conversation = Conversation(session_id=session_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        return conversation

    @staticmethod
    def add_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def update_filters(db: Session, conversation_id: int, filters: dict):
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            # Simple merge
            current = conversation.metadata_filters or {}
            current.update({k: v for k, v in filters.items() if v is not None})
            conversation.metadata_filters = current
            db.commit()
