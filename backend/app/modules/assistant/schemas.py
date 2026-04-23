from pydantic import BaseModel
from typing import List, Optional, Literal
from app.core.schemas import APIResponse

# Base schemas
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class FilterState(BaseModel):
    city: Optional[str] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    type: Optional[str] = None

class PropertyRecommendation(BaseModel):
    id: int
    city: str
    price: float
    bedrooms: int
    type: str
    availability: bool
    reason: str

# Request schemas
class ChatRequest(BaseModel):
    """Request schema for chat with assistant"""
    user_input: str
    session_id: str
    history: List[ChatMessage] = []

# Response data schema
class ChatResponseData(BaseModel):
    """Data part of chat response"""
    type: Literal["clarification", "recommendation", "no_results"]
    message: str
    filters: FilterState
    recommendations: List[PropertyRecommendation] = []

# Response schemas
class ChatResponse(APIResponse[ChatResponseData]):
    """Response schema for chat with assistant"""
    pass
