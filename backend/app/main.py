from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.properties.router import router as properties_router
from app.modules.assistant.router import router as assistant_router
from app.modules.conversations.router import router as conversation_router

app = FastAPI(
    title="Real Estate Assistant API",
    description="Modular Monolith API for an AI-powered real estate assistant",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(properties_router, prefix="/api/v1/properties", tags=["Properties"])
app.include_router(assistant_router, prefix="/api/v1/assistant", tags=["Assistant"])
app.include_router(conversation_router, prefix="/api/v1/conversations", tags=["Conversations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Real Estate Assistant API", "docs": "/docs"}
