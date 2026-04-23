from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PropertyBase(BaseModel):
    city: str
    price: float
    bedrooms: int
    property_type: str
    availability: bool = True
    description: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    city: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    property_type: Optional[str] = None
    availability: Optional[bool] = None
    description: Optional[str] = None

class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
