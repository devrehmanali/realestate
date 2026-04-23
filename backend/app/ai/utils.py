from typing import Any
from app.modules.assistant.schemas import FilterState
from app.modules.properties.models import Property
from .constants import (
    PROPERTY_CARD_TEMPLATE,
    MAX_PROPERTIES_SHOWN,
    SYSTEM_ROLE,
    PROPERTY_RECOMMENDATION_PROMPT,
)


def normalize_message_history(history: list[Any]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []

    for item in history:
        if isinstance(item, dict):
            messages.append(
                {
                    "role": item.get("role", "user"),
                    "content": item.get("content", ""),
                }
            )
            continue

        role = getattr(item, "role", "user")
        content = getattr(item, "content", "")
        messages.append({"role": role, "content": content})

    return messages


def format_property_card(property_obj: Property) -> str:
    """Format a single property as a readable card."""
    availability_status = "Available" if property_obj.availability else "Not Available"
    description_line = f"   • {property_obj.description}" if property_obj.description else ""

    return PROPERTY_CARD_TEMPLATE.format(
        property_type=property_obj.property_type,
        city=property_obj.city,
        price=property_obj.price,
        bedrooms=property_obj.bedrooms,
        availability_status=availability_status,
        description_line=description_line,
    )


def render_properties_for_rag(properties: list[Property]) -> str:
    """Render properties in a readable format for RAG/LLM input."""
    if not properties:
        return "No properties match the requested filters."

    limited_properties = properties[: MAX_PROPERTIES_SHOWN + 2]
    cards = [format_property_card(p) for p in limited_properties]

    return "\n\n".join(cards)


def format_filters_summary(filters: FilterState) -> str:
    """Create a summary of the current filter state."""
    parts = []
    if filters.city:
        parts.append(f"Location: {filters.city}")
    if filters.max_price:
        parts.append(f"Max Price: ${filters.max_price:,.0f}")
    if filters.bedrooms:
        parts.append(f"Bedrooms: {filters.bedrooms}")
    if filters.type:
        parts.append(f"Type: {filters.type}")

    return " | ".join(parts) if parts else "No specific filters"


def build_property_agent_prompt(
    filters: FilterState, properties: list[Property]
) -> str:
    """Build a RAG-style prompt for the property recommendation agent."""
    rendered_properties = render_properties_for_rag(properties)
    filters_summary = format_filters_summary(filters)

    city_display = filters.city or "selected area"
    max_price_display = f"${filters.max_price:,.0f}" if filters.max_price else "any budget"
    bedrooms_display = f"{filters.bedrooms} bedroom(s)" if filters.bedrooms else "any size"
    type_display = filters.type or "any type"

    return PROPERTY_RECOMMENDATION_PROMPT.format(
        city=city_display,
        max_price=max_price_display,
        bedrooms=bedrooms_display,
        property_type=type_display,
        properties_summary=rendered_properties,
    )


def build_conversation_context(
    history: list[Any], filters: FilterState, properties: list[Property]
) -> str:
    """Build conversation context for RAG-aware responses."""
    from .constants import CONVERSATION_SYSTEM

    rendered_properties = render_properties_for_rag(properties)
    filters_display = format_filters_summary(filters)

    return CONVERSATION_SYSTEM.format(
        filters=filters_display, properties=rendered_properties
    )
