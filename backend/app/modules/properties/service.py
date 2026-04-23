from sqlalchemy.orm import Session
from .models import Property
from .schemas import PropertyCreateRequest, PropertyUpdateRequest
from .seed_data import SEED_PROPERTIES
from typing import List, Optional

class PropertyService:
    @staticmethod
    def get_properties(
        db: Session, 
        city: Optional[str] = None, 
        max_price: Optional[float] = None, 
        bedrooms: Optional[int] = None,
        property_type: Optional[str] = None
    ) -> List[Property]:
        query = db.query(Property)
        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))
        if max_price:
            query = query.filter(Property.price <= max_price)
        if bedrooms:
            query = query.filter(Property.bedrooms == bedrooms)
        if property_type:
            query = query.filter(Property.property_type.ilike(f"%{property_type}%"))
        
        return query.all()

    @staticmethod
    def create_property(db: Session, property_data: PropertyCreateRequest) -> Property:
        db_property = Property(**property_data.dict())
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property

    @staticmethod
    def get_property_by_id(db: Session, property_id: int) -> Optional[Property]:
        return db.query(Property).filter(Property.id == property_id).first()

    @staticmethod
    def update_property(db: Session, property_id: int, property_data: PropertyUpdateRequest) -> Optional[Property]:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if property_obj:
            for key, value in property_data.dict(exclude_unset=True).items():
                setattr(property_obj, key, value)
            db.commit()
            db.refresh(property_obj)
        return property_obj

    @staticmethod
    def delete_property(db: Session, property_id: int) -> bool:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if property_obj:
            db.delete(property_obj)
            db.commit()
            return True
        return False

    @staticmethod
    def seed_data(db: Session) -> int:
        """Seed the database with initial property data. Returns number of records added."""
        # Check if data already exists
        if db.query(Property).count() > 0:
            return 0  # Already seeded

        # Add seed properties
        added_count = 0
        for prop_data in SEED_PROPERTIES:
            try:
                property_obj = Property(**prop_data)
                db.add(property_obj)
                added_count += 1
            except Exception as e:
                print(f"Error adding property {prop_data}: {e}")
                continue

        db.commit()
        return added_count
