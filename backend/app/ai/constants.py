"""AI agent constants, prompts, and configuration for the property recommendation system."""

# ============================================================================
# System Instructions
# ============================================================================
SYSTEM_ROLE = """You are a professional, friendly real estate assistant AI. Your role is to:
1. Help users find properties that match their needs and budget
2. Provide personalized recommendations based on their preferences
3. Answer questions about properties, locations, and real estate market
4. Guide users through the property search process
5. Maintain context from the conversation history

Always be helpful, professional, and concise. Provide clear reasoning for why a property is recommended.
When recommending properties, explain how each matches the user's criteria."""

# ============================================================================
# Conversation Context
# ============================================================================
CONVERSATION_SYSTEM = """You are analyzing a conversation about real estate property search.
Based on the conversation history, understand the user's requirements and preferences.
Current filters extracted: {filters}
Available properties that match: {properties}

Provide a helpful, concise response that acknowledges their preferences and explains why the shown properties are good matches."""

# ============================================================================
# Property Recommendation Prompt
# ============================================================================
PROPERTY_RECOMMENDATION_PROMPT = """Based on the user's request and filters, provide a personalized recommendation message.

User's Criteria:
- Location: {city}
- Max Budget: ${max_price}
- Bedrooms: {bedrooms}
- Property Type: {property_type}

Available Matches:
{properties_summary}

Guidelines:
1. Explain why these properties match their criteria
2. Highlight the best features or value propositions
3. Mention any special advantages (location, price, amenities)
4. Suggest next steps (view more, contact agent, apply filters)
5. Be warm and encouraging

Return a natural, conversational recommendation message."""

# ============================================================================
# Clarification Prompts
# ============================================================================
CLARIFICATION_NEEDED = "To help you find the perfect property, I need a bit more information."

CLARIFICATION_MESSAGES = {
    "city": "Which city or area are you looking to find a property in?",
    "price": "What is your maximum budget for the property?",
    "type": "Are you looking for an apartment, villa, house, studio, or something else?",
    "bedrooms": "How many bedrooms do you need?",
}

# ============================================================================
# No Results Handler
# ============================================================================
NO_RESULTS_MESSAGE = """I couldn't find any {property_type} in {city} within your budget of ${max_price}.

Here are some suggestions:
1. Expand your budget range
2. Try a nearby area
3. Consider a different property type
4. Adjust the number of bedrooms

Would you like to modify any of these preferences?"""

# ============================================================================
# Property Summary Template
# ============================================================================
PROPERTY_CARD_TEMPLATE = """📍 **{property_type.title()}** in {city}
   • Price: ${price:,.0f}
   • Bedrooms: {bedrooms}
   • Status: {availability_status}
   {description_line}"""

# ============================================================================
# Context Window Configuration
# ============================================================================
MAX_CONVERSATION_HISTORY = 10  # Keep last N messages for context
MAX_PROPERTIES_SHOWN = 5  # Show max 5 properties in recommendations

# ============================================================================
# Response Types
# ============================================================================
RESPONSE_TYPE_CLARIFICATION = "clarification"
RESPONSE_TYPE_RECOMMENDATION = "recommendation"
RESPONSE_TYPE_NO_RESULTS = "no_results"
RESPONSE_TYPE_ERROR = "error"

# ============================================================================
# Filter Extraction Rules
# ============================================================================
VALID_CITIES = [
    "riyadh",
    "jeddah",
    "dammam",
    "khobar",
    "mecca",
    "medina",
]

VALID_PROPERTY_TYPES = [
    "apartment",
    "villa",
    "house",
    "studio",
    "duplex",
]

PRICE_THRESHOLD_MIN = 10000  # Minimum recognizable price
BEDROOM_THRESHOLD = 10  # Maximum reasonable bedrooms

# ============================================================================
# Error Messages
# ============================================================================
ERROR_AI_SERVICE = "I encountered an issue while processing your request. Please try again."
ERROR_DATABASE = "I'm having trouble accessing the property database. Please try again."
ERROR_AGENT_INIT = "The AI assistant is not properly initialized."
