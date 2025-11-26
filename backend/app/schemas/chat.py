from pydantic import BaseModel
from typing import List, Optional

# This defines a single message in conversation
class MessageSchema(BaseModel):
    role: str          # Either "user" or "assistant"
    content: str       # The actual message text

# This is what the frontend SENDS to the backend
class ChatRequestSchema(BaseModel):
    message: str
    conversation_history: List  # define properly as list of messages
    mode: Optional[str] = "casual"  # default to casual

# This is what the backend SENDS back to the frontend
class ChatResponseSchema(BaseModel):
    response: str      # The AI's answer
    sources: List[str] = []  # Where the answer came from (e.g., "fastapi_docs")
