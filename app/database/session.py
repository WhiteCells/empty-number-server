from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from config import Config

DATABASE_URL = Config.DATABASE_URL()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
