from fastapi import HTTPException, Request
from app.ai.agent import PropertyAgent


def get_property_agent(request: Request) -> PropertyAgent:
    agent = getattr(request.app.state, "property_agent", None)
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="AI service is not available. The property agent is not initialized.",
        )
    return agent
