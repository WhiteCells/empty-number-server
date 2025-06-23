from typing import AsyncGenerator
from redis.asyncio import Redis
import redis.asyncio as aioredis
from app.config import Config

redis_client = aioredis.from_url(url=Config.REDIS_URL(),
                         max_connections=Config.REDIS_MAX_CONN,
                         decode_responses=True)

async def provide_redis_client() -> AsyncGenerator[Redis, None]:
    yield redis_client
