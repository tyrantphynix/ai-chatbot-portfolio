from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequestSchema, ChatResponseSchema
from app.services.retriever_service import retriever_service
from typing import List

router = APIRouter(tags=["chat"])

# In-memory conversation history (for demo - use database for production)
conversation_history: List[dict] = []

@router.post("/chat", response_model=ChatResponseSchema)
async def chat(request: ChatRequestSchema):
    """Main chat endpoint using RAG"""
    try:
        # Get user message
        user_message = request.message
        
        # Retrieve and generate answer
        result = retriever_service.retrieve_and_answer(user_message)
        
        # Extract answer
        answer = result["answer"]
        
        # Format sources
        sources = [meta.get("source", "unknown") for meta in result["sources"]]
        
        # Store in history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": answer})
        
        return ChatResponseSchema(
            response=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
async def get_history():
    """Get conversation history"""
    return {"messages": conversation_history}

@router.delete("/chat/history")
async def clear_history():
    """Clear conversation history"""
    conversation_history.clear()
    return {"message": "History cleared"}
