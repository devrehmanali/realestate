from pydantic import BaseModel
from typing import Any, Optional, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """Unified API Response Schema"""
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[list[str]] = None

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    """Error Response Schema"""
    success: bool = False
    message: str
    errors: Optional[list[str]] = None

class SuccessResponse(BaseModel, Generic[T]):
    """Success Response Schema"""
    success: bool = True
    message: str
    data: T

# Pagination schemas
class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated Response Schema"""
    success: bool = True
    message: str
    data: list[T]
    meta: PaginationMeta