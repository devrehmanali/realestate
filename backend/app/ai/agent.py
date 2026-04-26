import json
from typing import Any
from app.modules.assistant.schemas import FilterState
from app.modules.properties.models import Property
from .openrouter_client import OpenRouterClient
from .utils import (
    build_property_agent_prompt,
    normalize_message_history,
    build_conversation_context,
    render_properties_for_rag,
    format_filters_summary
)
from .constants import SYSTEM_ROLE, MAX_CONVERSATION_HISTORY


class PropertyAgent:
    """Context-aware property recommendation agent using OpenRouter."""

    def __init__(self, client: OpenRouterClient):
        self.client = client

    def _prepare_message_history(self, history: list[Any]) -> list[dict[str, str]]:
        """Prepare conversation history for the LLM, limiting to recent context."""
        messages = normalize_message_history(history)
        # Keep only recent messages for context window
        if len(messages) > MAX_CONVERSATION_HISTORY:
            messages = messages[-MAX_CONVERSATION_HISTORY :]
        return messages

    def extract_filters(
        self,
        latest_user_input: str,
        current_filters: FilterState,
    ) -> FilterState:
        """Extract property search filters using the LLM."""
        prompt = f"""Extract property search filters from the user's latest message, combining them with current filters if they are not explicitly overridden.
Current Filters: {current_filters.dict()}
Latest User Message: {latest_user_input}

Extract the following:
- city (string, null if unknown)
- max_price (float, null if unknown)
- bedrooms (int, null if unknown)
- type (string, null if unknown, like 'apartment', 'villa', 'studio', etc.)

Return ONLY a valid JSON object matching this schema:
{{"city": "...", "max_price": ..., "bedrooms": ..., "type": "..."}}
"""
        try:
            response = self.client.chat([{"role": "user", "content": prompt}], temperature=0.0)
            print(f"DEBUG: Extract Filters Prompt: {prompt}")
            print(f"DEBUG: Extract Filters Response: {response}")
            
            import re
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                data = json.loads(response)
                
            # Safely extract valid fields
            return FilterState(
                city=data.get("city"),
                max_price=data.get("max_price"),
                bedrooms=data.get("bedrooms"),
                type=data.get("type")
            )
        except Exception as e:
            print(f"DEBUG: Extract Filters Exception: {e}")
            # Fallback
            from app.modules.assistant.processor import IntentProcessor
            return IntentProcessor().extract_filters(latest_user_input, current_filters)

    def generate_recommendation_message(
        self,
        filters: FilterState,
        properties: list[Property],
        history: list[Any],
        latest_user_input: str,
    ) -> str:
        """Generate a personalized property recommendation using RAG."""
        
        prepared_history = self._prepare_message_history(history)
        
        filters_summary = format_filters_summary(filters)
        properties_summary = render_properties_for_rag(properties)
        
        context_msg = f"Current User Filters: {filters_summary}\\n\\nAvailable Properties Matching Filters:\\n{properties_summary}\\n\\nBased on the conversation history and the user's latest message, respond naturally. If the user is asking a question about a specific property or anything else, answer it. If they are looking for recommendations, use the 'Available Properties' to suggest options. If no properties match, suggest adjusting the filters."

        messages = [
            {"role": "system", "content": f"{SYSTEM_ROLE}\\n\\n{context_msg}"},
            *prepared_history,
            {
                "role": "user",
                "content": latest_user_input,
            },
        ]

        # Call the LLM with OpenRouter
        response = self.client.chat(messages, temperature=0.7)
        return response
