from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.core.schemas import APIResponse

# Base schemas
class MessageBase(BaseModel):
    role: str
    content: str

class ConversationBase(BaseModel):
    session_id: str
    metadata_filters: Dict[str, Any] = {}

# Request schemas
class ConversationCreateRequest(ConversationBase):
    """Request schema for creating a conversation"""
    pass

class MessageCreateRequest(MessageBase):
    """Request schema for creating a message"""
    conversation_id: int

class ConversationFiltersUpdateRequest(BaseModel):
    """Request schema for updating conversation filters"""
    filters: Dict[str, Any]

# Response schemas
class MessageResponse(MessageBase):
    """Response schema for message data"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationResponse(ConversationBase):
    """Response schema for conversation data"""
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class MessageCreateResponse(APIResponse[MessageResponse]):
    """Response schema for creating a message"""
    pass

class ConversationCreateResponse(APIResponse[ConversationResponse]):
    """Response schema for creating a conversation"""
    pass

class ConversationGetResponse(APIResponse[ConversationResponse]):
    """Response schema for getting a conversation"""
    pass

class ConversationFiltersUpdateResponse(APIResponse[ConversationResponse]):
    """Response schema for updating conversation filters"""
    pass
