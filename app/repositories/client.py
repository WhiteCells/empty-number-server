from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.client import CreateClientDto, PutClientDto
from app.models.client import Client, ClientStatus
from app.utils.logger import logger
from app.dto.api import NotifyDto


class ClientRepository:
    def __init__(self, db_session: AsyncSession, redis_client: Redis) -> None:
        self._db_session = db_session
        self._redis_client = redis_client

    async def notify(self, client_id: str, data: NotifyDto) -> tuple[dict, str]:
        # 判断 client 是否存在，这个 client_id 是 uuid，不是 id
        try:
            client = await self.get_client_by_uuid(client_id)
            if not client:
                # 新增 client
                client = Client(
                    uuid=client_id, 
                    threads_num=data.threads_num
                )
                self._db_session.add(client)
                await self._db_session.commit()
                await self._db_session.flush()
            else:
                # 更新 client
                client.status = ClientStatus.Online
                client.threads_num = data.threads_num
                await self._db_session.commit()
                await self._db_session.flush()
            logger.info(f"client {client.id} notify")

            # 新增或更新 client 的 redis 记录
            await self._update_client_redis(
                client_id, 
                ClientStatus.Online, 
                data.threads_num)

            return {"client_id": client.id}, None
        except Exception as e:
            await self._db_session.rollback()
            return None, f"接收客户端通知失败{e}"

    async def get_client_by_uuid(self, uuid: str) -> dict:
        res = await self._db_session.execute(
            select(Client).where(Client.uuid == uuid)
        )
        return res.scalar_one_or_none()
    
    async def _update_client_redis(self, uuid: str, status: str, threads_num: int):
        key = f"client:{uuid}"
        await self._redis_client.hset(key, mapping={
            "status": status,
            "threads_num": threads_num
        })
        await self._redis_client.expire(key, 10)

    async def _get_client_redis(self, uuid: str):
        key = f"client:{uuid}"
        return await self._redis_client.hgetall(key)

async def provide_client_repository(db_session: AsyncSession, redis_client: Redis) -> AsyncGenerator[ClientRepository, None]:
    yield ClientRepository(db_session, redis_client)
