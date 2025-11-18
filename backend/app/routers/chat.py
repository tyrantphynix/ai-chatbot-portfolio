from fastapi import APIRouter
from app.schemas.chat import ChatRequestSchema, ChatResponseSchema

# Create a router for all chat-related endpoints
router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponseSchema)
async def chat(request: ChatRequestSchema):
    # Placeholder - will implement in Phase 3
    return {"response": "Coming soon", "sources": []}

@router.get("/chat/history")
async def get_history():
    return {"messages": []}
