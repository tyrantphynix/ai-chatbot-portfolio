from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Groq API Configuration
    GROQ_API_KEY: str
    
    # ChromaDB Configuration
    CHROMA_DATA_PATH: str = "./chroma_data"
    
    # Application Configuration
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Chatbot"
    
    class Config:
        env_file = ".env"

settings = Settings()
