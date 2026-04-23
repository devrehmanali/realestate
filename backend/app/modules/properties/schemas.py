from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.core.schemas import APIResponse, PaginatedResponse, PaginationMeta

# Base schemas
class PropertyBase(BaseModel):
    city: str
    price: float
    bedrooms: int
    property_type: str
    availability: bool = True
    description: Optional[str] = None

# Request schemas
class PropertyCreateRequest(PropertyBase):
    """Request schema for creating a property"""
    pass

class PropertyUpdateRequest(BaseModel):
    """Request schema for updating a property"""
    city: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    property_type: Optional[str] = None
    availability: Optional[bool] = None
    description: Optional[str] = None

class PropertyFiltersRequest(BaseModel):
    """Request schema for filtering properties"""
    city: Optional[str] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    property_type: Optional[str] = None

class SeedDataRequest(BaseModel):
    """Request schema for seeding data (empty body)"""
    pass

# Response schemas
class PropertyResponse(PropertyBase):
    """Response schema for property data"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PropertyListResponse(PaginatedResponse[PropertyResponse]):
    """Response schema for listing properties"""
    pass

class PropertyCreateResponse(APIResponse[PropertyResponse]):
    """Response schema for creating a property"""
    pass

class PropertyUpdateResponse(APIResponse[PropertyResponse]):
    """Response schema for updating a property"""
    pass

class SeedDataResponse(APIResponse[dict]):
    """Response schema for seeding data"""
    pass
