import re
from typing import Optional
from .schemas import FilterState
from app.ai.constants import (
    VALID_CITIES,
    VALID_PROPERTY_TYPES,
    PRICE_THRESHOLD_MIN,
    BEDROOM_THRESHOLD,
    CLARIFICATION_MESSAGES,
)


class IntentProcessor:
    def __init__(self):
        self.cities = VALID_CITIES
        self.types = VALID_PROPERTY_TYPES

    def extract_filters(self, text: str, current_filters: FilterState) -> FilterState:
        """Extract property filters from user input using pattern matching."""
        text = text.lower()

        # Extract city
        extracted_city = current_filters.city
        for city in self.cities: # Need to match regex here 
            if city in text:
                extracted_city = city.capitalize()
                break

        # Extract property type
        extracted_type = current_filters.type
        for prop_type in self.types:
            if prop_type in text:
                extracted_type = prop_type.capitalize()
                break

        # Extract price (look for numbers that could be budget)
        extracted_price = current_filters.max_price
        prices = re.findall(r"(\d+[\d,.]*)", text) # Need to match regex here 
        for p in prices:
            val = float(p.replace(",", "").replace(".", ""))
            if val > PRICE_THRESHOLD_MIN:
                extracted_price = val
                break

        # Extract bedrooms (look for patterns like "2 bedroom", "3 br", etc.)
        extracted_bedrooms = current_filters.bedrooms
        bedroom_matches = re.findall(r"(\d+)\s*(?:bedroom|br|bed|room)", text)
        if bedroom_matches:
            bd_count = int(bedroom_matches[0])
            if 0 < bd_count <= BEDROOM_THRESHOLD:
                extracted_bedrooms = bd_count

        return FilterState(
            city=extracted_city,
            max_price=extracted_price,
            bedrooms=extracted_bedrooms,
            type=extracted_type,
        )

    def needs_clarification(self, filters: FilterState) -> Optional[str]:
        """Determine if clarification is needed and return appropriate message."""
        # Check filters in priority order
        if not filters.city:
            return CLARIFICATION_MESSAGES.get("city", "Which city are you looking in?")
        if not filters.max_price:
            return CLARIFICATION_MESSAGES.get("price", "What is your budget?")
        if not filters.type:
            return CLARIFICATION_MESSAGES.get("type", "What type of property are you looking for?")

        return None
