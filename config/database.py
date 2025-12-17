from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config.settings import settings
import os


# Database configuration that uses lazy initialization
DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
SYNC_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

# These will be initialized when get_engine() is called
engine = None
AsyncSessionLocal = None
sync_engine = None
SessionLocal = None
Base = declarative_base()


def get_engine():
    """Lazily initialize the database engine with fallback to SQLite"""
    global engine, AsyncSessionLocal, sync_engine, SessionLocal
    
    if engine is not None:
        return engine, AsyncSessionLocal, sync_engine, SessionLocal
    
    try:
        # Try to create async engine with PostgreSQL
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        engine = create_async_engine(DATABASE_URL)
        AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
        
        # Sync engine for Alembic migrations
        sync_engine = create_engine(SYNC_DATABASE_URL)
        SessionLocal = async_sessionmaker(sync_engine, expire_on_commit=False)
    except:
        # Fallback to SQLite if PostgreSQL is not available
        sqlite_url = "sqlite+aiosqlite:///./rag_system.db"
        sqlite_sync_url = "sqlite:///./rag_system.db"
        
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        engine = create_async_engine(sqlite_url)
        AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
        
        # Sync engine for Alembic migrations
        sync_engine = create_engine(sqlite_sync_url)
        SessionLocal = async_sessionmaker(sync_engine, expire_on_commit=False)
    
    return engine, AsyncSessionLocal, sync_engine, SessionLocal


def get_db():
    """Dependency to get DB session"""
    _, AsyncSessionLocal, _, _ = get_engine()
    db_gen = AsyncSessionLocal()
    try:
        yield db_gen
    finally:
        db_gen.close()