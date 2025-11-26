from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequestSchema, ChatResponseSchema
from app.services.retriever_service import retriever_service
from typing import List

router = APIRouter(tags=["chat"])

# In-memory conversation history (for demo - use database for production)
conversation_history: List[dict] = []

@router.post("/chat", response_model=ChatResponseSchema)
async def chat(request: ChatRequestSchema):
    """Main chat endpoint using multi-mode retrieval"""
    try:
        user_message = request.message
        print(f"DEBUG: User message: {user_message}")
        
        mode = request.mode or "casual"
    
        # Route based on selected mode instead of auto-classify
        if mode.lower() == "casual":
            result = retriever_service._handle_casual(user_message)
        elif mode.lower() == "realtime":
            result = retriever_service._handle_realtime(user_message)
        else:  # knowledge
            result = retriever_service._handle_knowledge(user_message)
        
        
        print(f"DEBUG: Result: {result}")
        
        # Extract answer
        answer = result["answer"]
        
        # Format sources
        sources = result.get("sources", [])
        
        # Store in history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": answer})
        
        return ChatResponseSchema(
            response=answer,
            sources=sources
        )
    except Exception as e:
        import traceback
        print(f"ERROR in chat endpoint: {e}")
        print(traceback.format_exc())  # Full traceback
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
