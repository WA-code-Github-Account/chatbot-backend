import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text  # <- ye add karo

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_5IXGHa8EAjNi@ep-rough-recipe-adwyzpd0-pooler.c-2.us-east-1.aws.neon.tech:5432/neondb"

engine = create_async_engine(DATABASE_URL, echo=True)

async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))  # <- wrap in text()
        print("Database connected, result:", result.scalar())

asyncio.run(test_connection())
