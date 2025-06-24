import threading
import asyncio
from collections import deque
from typing import Callable, Any
from sqlalchemy import select
from app.utils.database.session import async_session
from app.models.dialplan import Dialplan


class SafeQueue:
    def __init__(self, fetcher: Callable[[], asyncio.Future], interval: int = 10):
        self._queue = deque()
        self._lock = threading.Lock()
        self._fetcher = fetcher
        self._interval = interval
        self._ready = threading.Event()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def put(self, item: Any):
        with self._lock:
            self._queue.append(item)

    def put_many(self, items: list[Any]):
        with self._lock:
            self._queue.extend(items)

    def get(self, count: int = 1) -> list[Any]:
        with self._lock:
            items = []
            while self._queue and len(items) < count:
                items.append(self._queue.popleft())
            return items

    def size(self) -> int:
        with self._lock:
            return len(self._queue)

    def empty(self) -> bool:
        return self.size() == 0

    def wait_until_ready(self, timeout: int = 5) -> bool:
        return self._ready.wait(timeout)

    def _run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._load_worker(loop))

    async def _load_worker(self, loop: asyncio.AbstractEventLoop):
        while True:
            try:
                items = await self._fetcher()
                if items:
                    self.put_many(items)
                    if not self._ready.is_set():
                        self._ready.set()
            except Exception as e:
                print(f"[SafeQueue] Fetch error: {e}")
            await asyncio.sleep(self._interval)


async def fetch_free_dialplans(limit=10) -> list:
    async with async_session() as session:
        result = await session.execute(
            select(Dialplan).where(Dialplan.status == "free").limit(limit)
        )
        return result.scalars().all()


# 测试：
# async def fetch_free_dialplans(limit=10) -> list:
#     # await asyncio.sleep(0.1)
#     return ["111", "222", "333"]


if __name__ == "__main__":
    import time

    queue = SafeQueue(fetcher=fetch_free_dialplans, interval=10)

    if queue.wait_until_ready(timeout=1):
        plans = queue.get(count=3)
        for plan in plans:
            print("Fetched plan:", plan)
        if queue.empty():
            print("队列已空")
        else:
            print("队列剩余:", queue.size())
    else:
        print("超时：数据加载失败")
