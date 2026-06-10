"""Database connection and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0
    }
)
# pylint: disable=invalid-name
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    """Dependency to get a database session."""
    async with AsyncSessionLocal() as session:
        yield session
