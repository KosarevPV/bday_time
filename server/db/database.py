from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from server.config import settings

# engine = create_async_engine(settings.ASYNC_DATABASE_URL)
engine = create_async_engine(settings.ASYNC_DATABASE_URL)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)
