from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from uuid import UUID

from config.database import Base, get_engine
from config.settings import settings
from src.api.v1.endpoints.rag import router as rag_router
from src.models.user import User  # Adjust the import based on your actual model structure
from src.models.user_query import UserQuery  # Adjust the import based on your actual model structure
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from utils.password_utils import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    This will run startup and shutdown events.
    """
    logger.info("Starting up the application...")

    # Initialize database engine
    engine, async_sessionmaker, sync_engine, sessionmaker = get_engine()

    # Create database tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    # Create default user if it doesn't exist
    try:
        await create_default_user(async_sessionmaker)
        logger.info("Default user creation process completed")
    except Exception as e:
        logger.error(f"Error creating default user: {e}")
        raise

    yield  # Application runs here

    # Shutdown events would go here if needed
    logger.info("Shutting down the application...")


async def create_default_user(async_sessionmaker):
    """
    Creates a default user if it doesn't exist in the database.
    This is necessary to prevent foreign key constraint violations.
    """
    from sqlalchemy import select

    # Generate a proper password hash for the default user
    default_password = "default_password_123"  # You can change this to any default password
    default_hashed_password = hash_password(default_password)

    async with async_sessionmaker() as session:
        # Define the default user details
        default_user_id = UUID("12345678-1234-5678-1234-123456789abc")
        default_username = "Guest User"
        default_user_email = "guest@example.com"

        # Check if the user already exists
        stmt = select(User).where(User.id == default_user_id)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.info(f"Default user already exists with ID: {default_user_id}")
            return

        # Create the default user
        try:
            default_user = User(
                id=default_user_id,
                username=default_username,
                email=default_user_email,
                hashed_password=default_hashed_password,
                role='user'
            )

            session.add(default_user)
            await session.commit()
            logger.info(f"Default user created with ID: {default_user_id}")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating default user: {e}")
            raise


# Create FastAPI app instance
app = FastAPI(
    title="Chatbot Backend API",
    description="Backend API for chatbot application with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(rag_router, prefix="/api/v1", tags=["rag"])

@app.get("/")
async def root():
    return {"message": "Chatbot Backend API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatbot-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    )