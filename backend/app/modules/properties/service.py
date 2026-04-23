from sqlalchemy.orm import Session
from .models import Property
from .schemas import PropertyCreate, PropertyUpdate
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
    def create_property(db: Session, property_data: PropertyCreate) -> Property:
        db_property = Property(**property_data.dict())
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property

    @staticmethod
    def seed_data(db: Session):
        # Initial data if table is empty
        if db.query(Property).count() == 0:
            initial_properties = [
                {"city": "Riyadh", "price": 450000, "bedrooms": 2, "property_type": "apartment", "description": "Modern apt in city center"},
                {"city": "Riyadh", "price": 1200000, "bedrooms": 4, "property_type": "villa", "description": "Luxury villa with pool"},
                {"city": "Jeddah", "price": 300000, "bedrooms": 1, "property_type": "apartment", "description": "Cozy studio near sea"},
                {"city": "Dammam", "price": 600000, "bedrooms": 3, "property_type": "house", "description": "Family home"},
            ]
            for p in initial_properties:
                db.add(Property(**p))
            db.commit()
