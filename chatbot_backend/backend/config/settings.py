from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database settings
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432

    # Qdrant settings
    qdrant_host: str
    qdrant_api_key: Optional[str] = None

    # API settings
    groq_api_key: str

    # Application settings
    app_name: str = "RAG System API"
    debug: bool = True
    port: int = 8000

    # CORS settings
    cors_origins: List[str] = [
        "https://hackhathon-1-2.vercel.app",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
