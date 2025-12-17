from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "rag_system_db"

    # Qdrant settings
    qdrant_host: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None

    # Groq API settings
    groq_api_key: str = "gsk_undefined_groq_api_key"

    # JWT settings
    secret_key: str = "your-secret-key-change-this-for-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application settings
    app_name: str = "RAG System API"
    debug: bool = True  # Enable debug mode for development
    
    class Config:
        env_file = ".env"


settings = Settings()