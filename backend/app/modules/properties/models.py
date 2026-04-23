from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    property_type = Column(String, nullable=False) # 'apartment', 'villa', etc.
    availability = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Property(id={self.id}, city={self.city}, type={self.property_type})>"
