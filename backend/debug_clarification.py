"""Detailed clarification logic debugging"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.modules.assistant.processor import IntentProcessor
from app.modules.assistant.schemas import FilterState

processor = IntentProcessor()

print("DETAILED CLARIFICATION LOGIC TEST\n")

test_cases = [
    FilterState(),
    FilterState(city="Riyadh"),
    FilterState(city="Riyadh", max_price=500000),
    FilterState(city="Riyadh", max_price=500000, type="Villa"),
]

for i, filters in enumerate(test_cases, 1):
    clarification = processor.needs_clarification(filters)
    print(f"Case {i}: {filters}")
    print(f"  Clarification needed: {clarification}")
    print()
