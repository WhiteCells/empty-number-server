import asyncio
from app.utils.fetch import (
    fetch_free_dialplans_to_queue,
    fetch_queued_to_queue
)


async def on_startup():
    # 从数据库拉取详情入队
    asyncio.create_task(fetch_free_dialplans_to_queue())
    # 将数据库中为入队状态的详情入队
    # 使用持久化队列不需要这步
    # asyncio.create_task(fetch_queued_to_queue())
