import threading
import json
from app.utils.redisclient.cluster_client import get_redis_cluster_client


class DialplanQueue:

    maxsize = 100

    def __init__(self):
        self.client = get_redis_cluster_client()
        self._lock = threading.Lock()

    def put(self, key: str, item: any):
        with self._lock:
            self.client.rpush(key, json.dumps(item))

    def put_many(self, key: str, items: list[any]):
        with self._lock:
            if items:
                self.client.rpush(key, *[json.dumps(i) for i in items])

    def get(self, key: str, count: int = 1) -> list[any]:
        with self._lock:
            result = []
            for _ in range(count):
                item = self.client.lpop(key)
                if item is None:
                    break
                result.append(json.loads(item))
            return result

    def size(self, key: str) -> int:
        with self._lock:
            return self.client.llen(key)

    def empty(self, key: str) -> bool:
        with self._lock:
            return self.size(key) == 0

    def clear(self, key: str):
        with self._lock:
            self.client.delete(key)

_dialplan_queue = None

def get_dialplan_queue() -> DialplanQueue:
    global _dialplan_queue
    if _dialplan_queue is None:
        _dialplan_queue = DialplanQueue()
    return _dialplan_queue

if __name__ == "__main__":
    queue = DialplanQueue()

    queue.put("taskA", "task1")
    queue.put_many("taskA", ["task2", "task3", "task4"])

    print("Fetched:", queue.get("taskA", 2))
    print("Remaining size:", queue.size("taskA"))
