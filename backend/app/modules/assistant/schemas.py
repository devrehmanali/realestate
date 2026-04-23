from pydantic import BaseModel
from typing import List, Optional, Literal

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    user_input: str
    session_id: str
    history: List[ChatMessage] = []

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

class ChatResponse(BaseModel):
    type: Literal["clarification", "recommendation", "no_results"]
    message: str
    filters: FilterState
    recommendations: List[PropertyRecommendation] = []
