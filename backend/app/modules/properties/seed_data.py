"""
Seed data generator for properties.
Generates realistic property data for Saudi Arabian cities.
"""
import random
from typing import List, Dict, Any

# Saudi Arabian cities with their approximate populations/regions
SAUDI_CITIES = [
    "Riyadh", "Jeddah", "Dammam", "Mecca", "Medina", "Khobar",
    "Taif", "Abha", "Jubail", "Yanbu", "Hail", "Tabuk",
    "Najran", "Al-Khobar", "Dhahran", "Al-Hasa"
]

PROPERTY_TYPES = ["apartment", "villa", "house", "studio", "penthouse", "townhouse"]

# Price ranges by city (approximate in SAR)
CITY_PRICE_RANGES = {
    "Riyadh": (200000, 5000000),
    "Jeddah": (150000, 4000000),
    "Dammam": (180000, 3500000),
    "Mecca": (120000, 2000000),
    "Medina": (130000, 2500000),
    "Khobar": (200000, 4500000),
    "Taif": (100000, 1800000),
    "Abha": (80000, 1500000),
    "Jubail": (160000, 3000000),
    "Yanbu": (140000, 2200000),
    "Hail": (90000, 1200000),
    "Tabuk": (85000, 1300000),
    "Najran": (70000, 1000000),
    "Al-Khobar": (190000, 4200000),
    "Dhahran": (180000, 3800000),
    "Al-Hasa": (120000, 2000000)
}

BEDROOM_OPTIONS = [1, 2, 3, 4, 5, 6]

DESCRIPTIONS = [
    "Modern apartment in prime location",
    "Spacious villa with garden",
    "Cozy studio perfect for singles",
    "Luxury penthouse with city views",
    "Family home in quiet neighborhood",
    "Contemporary townhouse design",
    "Traditional house with modern amenities",
    "Beachfront property with stunning views",
    "Downtown apartment close to amenities",
    "Suburban villa with large backyard",
    "High-rise apartment with facilities",
    "Renovated property in historic district",
    "New construction with latest features",
    "Affordable housing option",
    "Premium property in gated community",
    "Corner unit with extra windows",
    "Ground floor with private entrance",
    "Rooftop terrace available",
    "Underground parking included",
    "Fully furnished option available"
]

def generate_property_data() -> List[Dict[str, Any]]:
    """Generate realistic property data for seeding."""
    properties = []

    # Generate at least 30 properties with good distribution
    for i in range(35):  # Generate 35 to ensure variety
        city = random.choice(SAUDI_CITIES)
        property_type = random.choice(PROPERTY_TYPES)

        # Adjust bedroom count based on property type
        if property_type == "studio":
            bedrooms = 1
        elif property_type in ["apartment", "penthouse"]:
            bedrooms = random.choice([1, 2, 3])
        else:  # villa, house, townhouse
            bedrooms = random.choice([2, 3, 4, 5, 6])

        # Get price range for city
        min_price, max_price = CITY_PRICE_RANGES.get(city, (100000, 1000000))

        # Adjust price based on bedrooms and property type
        base_price = random.randint(min_price, max_price)
        if bedrooms > 3:
            base_price = int(base_price * 1.3)  # Larger properties cost more
        if property_type in ["villa", "penthouse"]:
            base_price = int(base_price * 1.4)  # Premium types cost more

        # Ensure price doesn't exceed reasonable limits
        price = min(base_price, max_price)

        # Generate description
        description = random.choice(DESCRIPTIONS)

        # Some properties are not available
        availability = random.choice([True, True, True, False])  # 75% available

        property_data = {
            "city": city,
            "price": price,
            "bedrooms": bedrooms,
            "property_type": property_type,
            "availability": availability,
            "description": description
        }

        properties.append(property_data)

    return properties

# Generate the seed data
SEED_PROPERTIES = generate_property_data()

if __name__ == "__main__":
    # Print sample data for verification
    print(f"Generated {len(SEED_PROPERTIES)} properties:")
    for i, prop in enumerate(SEED_PROPERTIES[:5], 1):
        print(f"{i}. {prop['city']} - {prop['property_type']} - {prop['bedrooms']}BR - SAR {prop['price']:,}")
    print("...")