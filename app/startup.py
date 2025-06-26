import asyncio
from app.utils.fetch import fetch_free_dialplans_to_queue


async def on_startup():
    asyncio.create_task(fetch_free_dialplans_to_queue())
