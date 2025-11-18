from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import chat

# Create FastAPI app instance
app = FastAPI(title=settings.PROJECT_NAME)

# Enable CORS (allows frontend to call backend from different domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the chat router (all endpoints in chat.py will be prefixed with /api/v1)
app.include_router(chat.router, prefix=settings.API_V1_STR)

# Health check endpoint (useful for monitoring)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
