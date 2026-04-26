from sqlalchemy.orm import Session
from app.ai.agent import PropertyAgent
from app.ai.constants import (
    ERROR_AI_SERVICE,
    RESPONSE_TYPE_RECOMMENDATION,
    MAX_PROPERTIES_SHOWN,
)
from app.modules.properties.service import PropertyService
from app.modules.conversations.service import ConversationService
from .schemas import (
    ChatRequest,
    ChatResponseData,
    FilterState,
    PropertyRecommendation,
)


class AssistantService:
    @classmethod
    def process_chat(
        cls,
        db: Session,
        request: ChatRequest,
        property_agent: PropertyAgent,
    ) -> ChatResponseData:
        """Process user chat message with context-aware property recommendations."""
        # 1. Access/Create Conversation
        conversation = ConversationService.get_or_create_conversation(
            db, request.session_id
        )

        # Extract history from DB before adding the new message
        db_history = [{"role": msg.role, "content": msg.content} for msg in conversation.messages]

        # 2. Add user message to history
        ConversationService.add_message(db, conversation.id, "user", request.user_input)

        # 3. Build current filter state from DB + extracted from current message
        db_filters = (
            FilterState(**conversation.metadata_filters)
            if conversation.metadata_filters
            else FilterState()
        )

        filters = property_agent.extract_filters(request.user_input, db_filters)

        # 4. Search Properties using extracted filters if any exist
        has_filters = any([filters.city, filters.max_price, filters.bedrooms, filters.type])
        properties = []
        if has_filters:
            properties = PropertyService.get_properties(
                db,
                city=filters.city,
                max_price=filters.max_price,
                bedrooms=filters.bedrooms,
                property_type=filters.type,
            )

        # 5. Generate AI-powered recommendation message using RAG
        try:
            message = property_agent.generate_recommendation_message(
                filters=filters,
                properties=properties,
                history=db_history,
                latest_user_input=request.user_input,
            )
        except Exception as e:
            message = ERROR_AI_SERVICE

        # 6. Build recommendation cards for the top properties
        recommendations = []
        if has_filters and properties:
            recommendations = [
                PropertyRecommendation(
                    id=p.id,
                    city=p.city,
                    price=p.price,
                    bedrooms=p.bedrooms,
                    type=p.property_type,
                    availability=p.availability,
                    reason=f"This {p.property_type.lower()} in {p.city} matches your criteria.",
                )
                for p in properties[:MAX_PROPERTIES_SHOWN]
            ]

        # 7. Update DB with assistant message and updated filters
        ConversationService.add_message(db, conversation.id, "assistant", message)
        ConversationService.update_filters(db, conversation.id, filters.dict())

        return ChatResponseData(
            type=RESPONSE_TYPE_RECOMMENDATION,
            message=message,
            filters=filters,
            recommendations=recommendations,
        )
