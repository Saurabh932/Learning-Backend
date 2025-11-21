"""
This file manages the database connection and initialization logic.
It uses SQLModel + SQLAlchemy's async engine to connect to PostgreSQL.
"""

from sqlmodel.ext.asyncio.session import AsyncSession  # ✅ from SQLModel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import config  # or wherever your DATABASE_URL lives


# ✅ Create an async engine (the correct function)
# Make sure your DATABASE_URL in .env uses an async driver:
#   - asyncpg:    postgresql+asyncpg://user:pass@host/db
#   - psycopg async: postgresql+psycopg_async://user:pass@host/db
async_engine = create_async_engine(
    config.DATABASE_URL,  # async DB URL from .env
    echo=False,            # Logs SQL queries (useful while developing)
)

# This function will be called at app startup to create tables if they don't exist.
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # Optional quick test SQL to confirm connection — commented out by default.
        # from sqlmodel import text
        # statement = text("SELECT 'hello';")
        # result = await conn.execute(statement)
        # print(result.all())

        # Create all tables defined by SQLModel models (Book, etc.)
        await conn.run_sync(SQLModel.metadata.create_all)


# Dependency function to provide an AsyncSession to FastAPI routes
async def get_session() -> AsyncSession:
    """
    Usage in routes:
        async def route(session: AsyncSession = Depends(get_session)):
            ...
    This yields a session that will be closed automatically after the request.
    """
    SessionLocal = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        yield session
