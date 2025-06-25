from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.client import CreateClientDto, PutClientDto, GetClientDto, GetClientsQueryDto
from app.models.client import Client, ClientStatus
from app.utils.logger import logger
from app.dto.api import NotifyDto
from datetime import timedelta
from app.utils.redisclient.cluster_client import get_redis_cluster_client


class ClientRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._redis_client = get_redis_cluster_client()

    async def notify(self, client_id: str, data: NotifyDto) -> tuple[dict, str]:
        try:
            # 判断 client 是否存在，这个 client_id 是 uuid，不是 id
            res = await self._db_session.execute(
                select(Client).where(Client.uuid == client_id)
            )
            client = res.scalar_one_or_none()
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
            self._update_client_redis(
                client_id, 
                ClientStatus.Online)

            return {"client_id": client.id}, None
        except Exception as e:
            await self._db_session.rollback()
            return None, f"接收客户端通知失败{e}"

    async def get_clients(self, query: GetClientsQueryDto) -> dict:
        return {}
        # offset = (query.page - 1) * query.size
        # limit = query.size
        # clients, total = await self._client_repository.get_clients(offset=offset, limit=limit)
        # if not clients:
        #     return {"clients": [], "total": total}, "No clients found"
        # return {"clients": clients, "total": total}, None

    async def get_client_by_uuid(self, uuid: str) -> dict:
        res = await self._db_session.execute(
            select(Client).where(Client.uuid == uuid)
        )
        client = res.scalar_one_or_none()
        if client is None:
            return None
        client_dict = GetClientDto.model_validate(client).model_dump()
        return client_dict
    
    async def heartbeat(self, client_id: str) -> bool:
        self._update_client_redis(client_id, ClientStatus.Online)
        return True
    
    async def get_client_by_id(self, id: int) -> dict:
        res = await self._db_session.execute(
            select(Client).where(Client.id == id)
        )
        client = res.scalar_one_or_none()
        if not client:
            return None
        client_dict = GetClientDto.model_validate(client).model_dump()
        return client_dict
    
    def _update_client_redis(self, uuid: str, status: str):
        key = f"client:{uuid}"
        self._redis_client.hset(key, mapping={
            "status": status
        })
        self._redis_client.expire(key, 10)

    async def _get_client_redis(self, uuid: str):
        key = f"client:{uuid}"
        return await self._redis_client.hgetall(key)

async def provide_client_repository(db_session: AsyncSession) -> AsyncGenerator[ClientRepository, None]:
    yield ClientRepository(db_session)
