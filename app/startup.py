import asyncio
from app.utils.fetch import (
    fetch_timeout_dialplans_to_queue,
    fetch_free_dialplans_to_queue,
    fetch_queued_to_queue
)


async def on_startup():
    asyncio.create_task(fetch_timeout_dialplans_to_queue())
    asyncio.create_task(fetch_free_dialplans_to_queue())
