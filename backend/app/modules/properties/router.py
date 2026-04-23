from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from .service import PropertyService
from .schemas import (
    PropertyListResponse, PropertyCreateRequest, PropertyCreateResponse,
    SeedDataResponse, PropertyUpdateRequest, PropertyUpdateResponse
)
from typing import Optional

router = APIRouter()

@router.get("/", response_model=PropertyListResponse)
def read_properties(
    city: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    properties = PropertyService.get_properties(db, city, max_price, bedrooms, property_type)
    return PropertyListResponse(
        success=True,
        message="Properties retrieved successfully",
        data=properties,
        meta={
            "page": 1,
            "per_page": len(properties),
            "total": len(properties),
            "total_pages": 1
        }
    )

@router.post("/", response_model=PropertyCreateResponse)
def create_property(property_data: PropertyCreateRequest, db: Session = Depends(get_db)):
    property_obj = PropertyService.create_property(db, property_data)
    return PropertyCreateResponse(
        success=True,
        message="Property created successfully",
        data=property_obj
    )

@router.get("/{property_id}", response_model=PropertyCreateResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property_obj = PropertyService.get_property_by_id(db, property_id)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyCreateResponse(
        success=True,
        message="Property retrieved successfully",
        data=property_obj
    )

@router.put("/{property_id}", response_model=PropertyUpdateResponse)
def update_property(property_id: int, property_data: PropertyUpdateRequest, db: Session = Depends(get_db)):
    property_obj = PropertyService.update_property(db, property_id, property_data)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyUpdateResponse(
        success=True,
        message="Property updated successfully",
        data=property_obj
    )

@router.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    success = PropertyService.delete_property(db, property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"success": True, "message": "Property deleted successfully"}

@router.post("/seed", response_model=SeedDataResponse)
def seed_properties(db: Session = Depends(get_db)):
    records_added = PropertyService.seed_data(db)
    if records_added == 0:
        return SeedDataResponse(
            success=True,
            message="Database already contains data, no new records added",
            data={"status": "already_seeded", "records_added": 0}
        )
    else:
        return SeedDataResponse(
            success=True,
            message=f"Database seeded successfully with {records_added} properties",
            data={"status": "completed", "records_added": records_added}
        )
