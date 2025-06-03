from typing import Optional, Any
import redis
from app.config import settings

class RedisUtils:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password
        )

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """
        设置键值对
        :param key: 键
        :param value: 值
        :param expire: 过期时间（秒）
        """
        self.redis_client.set(key, value)
        if expire:
            self.redis_client.expire(key, expire)

    def get(self, key: str) -> Optional[bytes]:
        """
        获取键对应的值
        :param key: 键
        :return: 值，如果不存在则返回 None
        """
        return self.redis_client.get(key)

    def delete(self, key: str) -> int:
        """
        删除键值对
        :param key: 键
        :return: 删除的键的数量
        """
        return self.redis_client.delete(key)

    def exists(self, key: str) -> bool:
        """
        检查键是否存在
        :param key: 键
        :return: 如果存在返回 True，否则返回 False
        """
        return self.redis_client.exists(key)
