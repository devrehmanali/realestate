from sqlalchemy.orm import Session
from app.modules.properties.service import PropertyService
from app.modules.conversations.service import ConversationService
from .processor import IntentProcessor
from .schemas import ChatRequest, ChatResponse, FilterState, PropertyRecommendation
from typing import List

class AssistantService:
    processor = IntentProcessor()

    @classmethod
    def process_chat(cls, db: Session, request: ChatRequest) -> ChatResponse:
        # 1. Access/Create Conversation
        conversation = ConversationService.get_or_create_conversation(db, request.session_id)
        
        # 2. Add user message to history
        ConversationService.add_message(db, conversation.id, "user", request.user_input)

        # 3. Build current filter state from DB + extracted from current message
        # Merging previous context
        db_filters = FilterState(**conversation.metadata_filters) if conversation.metadata_filters else FilterState()
        
        filters = cls.processor.extract_filters(request.user_input, db_filters)
        
        # 4. Check for clarification
        clarification_msg = cls.processor.needs_clarification(filters)
        
        response_type = "recommendation"
        recommendations = []
        message = ""

        if clarification_msg:
            response_type = "clarification"
            message = clarification_msg
        else:
            # 5. Search Properties
            properties = PropertyService.get_properties(
                db, 
                city=filters.city, 
                max_price=filters.max_price, 
                bedrooms=filters.bedrooms,
                property_type=filters.type
            )

            if not properties:
                response_type = "no_results"
                message = f"I couldn't find any {filters.type or 'properties'} in {filters.city} matching your budget. Would you like to try a different area or adjust your price range?"
            else:
                message = "I've found some great options for you!"
                recommendations = [
                    PropertyRecommendation(
                        id=p.id,
                        city=p.city,
                        price=p.price,
                        bedrooms=p.bedrooms,
                        type=p.property_type,
                        availability=p.availability,
                        reason=f"This {p.property_type} in {p.city} perfectly matches your budget of {filters.max_price}."
                    ) for p in properties[:3]
                ]

        # 6. Update DB with assistant message and updated filters
        ConversationService.add_message(db, conversation.id, "assistant", message)
        ConversationService.update_filters(db, conversation.id, filters.dict())

        return ChatResponse(
            type=response_type,
            message=message,
            filters=filters,
            recommendations=recommendations
        )
