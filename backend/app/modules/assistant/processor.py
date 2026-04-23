import re
from typing import Optional, Dict, Any
from .schemas import FilterState

class IntentProcessor:
    def __init__(self):
        self.cities = ["riyadh", "jeddah", "dammam", "khobar", "mecca", "medina"]
        self.types = ["apartment", "villa", "house", "studio", "duplex"]

    def extract_filters(self, text: str, current_filters: FilterState) -> FilterState:
        text = text.lower()
        
        extracted_city = current_filters.city
        for city in self.cities:
            if city in text:
                extracted_city = city.capitalize()
                break

        extracted_type = current_filters.type
        for prop_type in self.types:
            if prop_type in text:
                extracted_type = prop_type
                break

        # Extract price (simple heuristic: look for numbers > 1000)
        extracted_price = current_filters.max_price
        prices = re.findall(r'(\d+[\d,.]*)', text)
        for p in prices:
            val = float(p.replace(',', ''))
            if val > 10000: # Assuming budget
                extracted_price = val
            elif 0 < val <= 10: # Assuming bedrooms
                pass # Handled below

        # Extract bedrooms
        extracted_bedrooms = current_filters.bedrooms
        bedroom_matches = re.findall(r'(\d+)\s*(?:bedroom|br|room)', text)
        if bedroom_matches:
            extracted_bedrooms = int(bedroom_matches[0])

        return FilterState(
            city=extracted_city,
            max_price=extracted_price,
            bedrooms=extracted_bedrooms,
            type=extracted_type
        )

    def needs_clarification(self, filters: FilterState) -> Optional[str]:
        if not filters.city:
            return "Which city are you looking to find a property in?"
        if not filters.max_price:
            return f"What is your maximum budget for a property in {filters.city}?"
        if not filters.type:
            return f"Are you looking for an apartment, a villa, or something else in {filters.city}?"
        return None
