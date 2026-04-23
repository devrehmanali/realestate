from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from .service import PropertyService
from .schemas import PropertyResponse, PropertyCreate
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[PropertyResponse])
def read_properties(
    city: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return PropertyService.get_properties(db, city, max_price, bedrooms, property_type)

@router.post("/", response_model=PropertyResponse)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    return PropertyService.get_properties(db, property)

@router.post("/seed")
def seed_properties(db: Session = Depends(get_db)):
    PropertyService.seed_data(db)
    return {"message": "Database seeded successfully"}
