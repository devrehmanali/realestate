from typing import Any
from app.modules.assistant.schemas import FilterState
from app.modules.properties.models import Property
from .openrouter_client import OpenRouterClient
from .utils import (
    build_property_agent_prompt,
    normalize_message_history,
    build_conversation_context,
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

    def generate_recommendation_message(
        self,
        filters: FilterState,
        properties: list[Property],
        history: list[Any],
        latest_user_input: str,
    ) -> str:
        """Generate a personalized property recommendation using RAG."""
        # Build conversation context with properties and filters
        conversation_context = build_conversation_context(history, filters, properties)

        # Build RAG prompt with property details
        rag_prompt = build_property_agent_prompt(filters, properties)

        # Prepare message history
        prepared_history = self._prepare_message_history(history)

        # Construct messages for the LLM
        messages = [
            {"role": "system", "content": SYSTEM_ROLE},
            *prepared_history,
            {
                "role": "user",
                "content": f"{latest_user_input}\n\n{conversation_context}",
            },
            {
                "role": "user",
                "content": rag_prompt,
            },
        ]

        # Call the LLM with OpenRouter
        response = self.client.chat(messages, temperature=0.7)
        return response
