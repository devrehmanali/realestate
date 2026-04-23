from sqlalchemy.orm import Session
from app.ai.agent import PropertyAgent
from app.ai.constants import (
    NO_RESULTS_MESSAGE,
    ERROR_AI_SERVICE,
    RESPONSE_TYPE_CLARIFICATION,
    RESPONSE_TYPE_RECOMMENDATION,
    RESPONSE_TYPE_NO_RESULTS,
    MAX_PROPERTIES_SHOWN,
)
from app.modules.properties.service import PropertyService
from app.modules.conversations.service import ConversationService
from .processor import IntentProcessor
from .schemas import (
    ChatRequest,
    ChatResponseData,
    FilterState,
    PropertyRecommendation,
)


class AssistantService:
    processor = IntentProcessor()

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

        # 2. Add user message to history
        ConversationService.add_message(db, conversation.id, "user", request.user_input)

        # 3. Build current filter state from DB + extracted from current message
        # Merging previous context
        db_filters = (
            FilterState(**conversation.metadata_filters)
            if conversation.metadata_filters
            else FilterState()
        )

        filters = cls.processor.extract_filters(request.user_input, db_filters)

        # 4. Check for clarification
        clarification_msg = cls.processor.needs_clarification(filters)

        response_type = RESPONSE_TYPE_RECOMMENDATION
        recommendations = []
        message = ""

        if clarification_msg:
            response_type = RESPONSE_TYPE_CLARIFICATION
            message = clarification_msg
        else:
            # 5. Search Properties using extracted filters
            properties = PropertyService.get_properties(
                db,
                city=filters.city,
                max_price=filters.max_price,
                bedrooms=filters.bedrooms,
                property_type=filters.type,
            )

            if not properties:
                response_type = RESPONSE_TYPE_NO_RESULTS
                message = NO_RESULTS_MESSAGE.format(
                    property_type=filters.type or "property",
                    city=filters.city or "your area",
                    max_price=filters.max_price or 0,
                )
            else:
                # 6. Generate AI-powered recommendation message using RAG
                try:
                    message = property_agent.generate_recommendation_message(
                        filters=filters,
                        properties=properties,
                        history=request.history,
                        latest_user_input=request.user_input,
                    )
                except Exception as e:
                    message = ERROR_AI_SERVICE

                # 7. Build recommendation cards for the top properties
                recommendations = [
                    PropertyRecommendation(
                        id=p.id,
                        city=p.city,
                        price=p.price,
                        bedrooms=p.bedrooms,
                        type=p.property_type,
                        availability=p.availability,
                        reason=f"This {p.property_type.lower()} in {p.city} matches your criteria of {filters.bedrooms or 'any'} bedroom(s) and ${filters.max_price or 'any'} budget.",
                    )
                    for p in properties[:MAX_PROPERTIES_SHOWN]
                ]

        # 8. Update DB with assistant message and updated filters
        ConversationService.add_message(db, conversation.id, "assistant", message)
        ConversationService.update_filters(db, conversation.id, filters.dict())

        return ChatResponseData(
            type=response_type,
            message=message,
            filters=filters,
            recommendations=recommendations,
        )
