"""
Filter Verification Tests
Tests to verify that all filters are working correctly in the backend
"""

import sys
from pathlib import Path

# Add the app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.modules.assistant.processor import IntentProcessor
from app.modules.assistant.schemas import FilterState
from app.ai.constants import VALID_CITIES, VALID_PROPERTY_TYPES, PRICE_THRESHOLD_MIN

def test_city_extraction():
    """Test city filter extraction"""
    print("=" * 60)
    print("TEST 1: CITY FILTER EXTRACTION")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        ("I want a property in Riyadh", "Riyadh"),
        ("looking for houses in jeddah", "Jeddah"),
        ("Show me properties in dammam", "Dammam"),
        ("anything in khobar", "Khobar"),
        ("No city mentioned", None),
    ]
    
    for text, expected_city in test_cases:
        result = processor.extract_filters(text, FilterState())
        status = "✓ PASS" if result.city == expected_city else "✗ FAIL"
        print(f"{status}: '{text}'")
        print(f"   Expected: {expected_city}, Got: {result.city}")
    print()

def test_price_extraction():
    """Test price filter extraction"""
    print("=" * 60)
    print("TEST 2: PRICE FILTER EXTRACTION")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        ("budget of 500000 in Riyadh", 500000.0),
        ("I can spend 1,000,000", 1000000.0),
        ("max price is 750000", 750000.0),
        ("something under 300000", 300000.0),
        ("no budget mentioned", None),
    ]
    
    for text, expected_price in test_cases:
        result = processor.extract_filters(text, FilterState())
        status = "✓ PASS" if result.max_price == expected_price else "✗ FAIL"
        print(f"{status}: '{text}'")
        print(f"   Expected: {expected_price}, Got: {result.max_price}")
    print()

def test_bedroom_extraction():
    """Test bedroom filter extraction"""
    print("=" * 60)
    print("TEST 3: BEDROOM FILTER EXTRACTION")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        ("3 bedroom apartment", 3),
        ("2 br villa", 2),
        ("looking for 4 bedroom house", 4),
        ("1 bed studio", 1),
        ("no bedroom preference", None),
    ]
    
    for text, expected_bedrooms in test_cases:
        result = processor.extract_filters(text, FilterState())
        status = "✓ PASS" if result.bedrooms == expected_bedrooms else "✗ FAIL"
        print(f"{status}: '{text}'")
        print(f"   Expected: {expected_bedrooms}, Got: {result.bedrooms}")
    print()

def test_property_type_extraction():
    """Test property type filter extraction"""
    print("=" * 60)
    print("TEST 4: PROPERTY TYPE FILTER EXTRACTION")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        ("looking for an apartment", "Apartment"),
        ("i want a villa in Riyadh", "Villa"),
        ("show me houses", "House"),
        ("looking for a studio", "Studio"),
        ("no type mentioned", None),
    ]
    
    for text, expected_type in test_cases:
        result = processor.extract_filters(text, FilterState())
        status = "✓ PASS" if result.type == expected_type else "✗ FAIL"
        print(f"{status}: '{text}'")
        print(f"   Expected: {expected_type}, Got: {result.type}")
    print()

def test_combined_filter_extraction():
    """Test combined filter extraction"""
    print("=" * 60)
    print("TEST 5: COMBINED FILTER EXTRACTION")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        (
            "I want a 3 bedroom villa in Riyadh with a budget of 1,500,000",
            FilterState(city="Riyadh", max_price=1500000.0, bedrooms=3, type="Villa")
        ),
        (
            "2 bedroom apartment in Jeddah, not more than 750000",
            FilterState(city="Jeddah", max_price=750000.0, bedrooms=2, type="Apartment")
        ),
    ]
    
    for text, expected in test_cases:
        result = processor.extract_filters(text, FilterState())
        match = (
            result.city == expected.city and
            result.max_price == expected.max_price and
            result.bedrooms == expected.bedrooms and
            result.type == expected.type
        )
        status = "✓ PASS" if match else "✗ FAIL"
        print(f"{status}: '{text}'")
        print(f"   Expected: city={expected.city}, price={expected.max_price}, bedrooms={expected.bedrooms}, type={expected.type}")
        print(f"   Got: city={result.city}, price={result.max_price}, bedrooms={result.bedrooms}, type={result.type}")
    print()

def test_clarification_logic():
    """Test clarification message logic"""
    print("=" * 60)
    print("TEST 6: CLARIFICATION LOGIC")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    test_cases = [
        (FilterState(), "city"),  # Missing all, should ask for city first
        (FilterState(city="Riyadh"), "price"),  # Missing price
        (FilterState(city="Riyadh", max_price=500000), "type"),  # Missing type
        (FilterState(city="Riyadh", max_price=500000, type="Villa"), None),  # All required
    ]
    
    for filters, expected_missing in test_cases:
        clarification = processor.needs_clarification(filters)
        if expected_missing is None:
            status = "✓ PASS" if clarification is None else "✗ FAIL"
            print(f"{status}: Complete filters should not need clarification")
        else:
            has_keyword = expected_missing.lower() in (clarification or "").lower()
            status = "✓ PASS" if has_keyword else "✗ FAIL"
            print(f"{status}: Filters {filters} - expecting clarification about {expected_missing}")
            print(f"   Got: {clarification}")
    print()

def test_filter_persistence():
    """Test filter persistence/merging"""
    print("=" * 60)
    print("TEST 7: FILTER PERSISTENCE")
    print("=" * 60)
    
    processor = IntentProcessor()
    
    # Start with initial filters
    current_filters = FilterState(city="Riyadh", max_price=500000)
    print(f"Initial filters: {current_filters}")
    
    # Extract new filter while keeping old ones
    new_text = "I want 3 bedrooms"
    result = processor.extract_filters(new_text, current_filters)
    print(f"After 'I want 3 bedrooms': {result}")
    
    expected = FilterState(city="Riyadh", max_price=500000, bedrooms=3)
    match = (
        result.city == expected.city and
        result.max_price == expected.max_price and
        result.bedrooms == expected.bedrooms
    )
    status = "✓ PASS" if match else "✗ FAIL"
    print(f"{status}: Filters should persist")
    print()

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "FILTER VERIFICATION TESTS" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_city_extraction()
        test_price_extraction()
        test_bedroom_extraction()
        test_property_type_extraction()
        test_combined_filter_extraction()
        test_clarification_logic()
        test_filter_persistence()
        
        print("=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
    except Exception as e:
        print(f"ERROR during tests: {e}")
        import traceback
        traceback.print_exc()
