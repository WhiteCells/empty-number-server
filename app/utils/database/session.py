from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import Config


engine = create_async_engine(
    url=Config.DATABASE_URL(),
    pool_size=Config.MYSQL_POOL_SIZE,
    max_overflow=Config.MYSQL_POOL_TEMP,
    pool_recycle=Config.MYSQL_POOL_RECYCLE, 
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session