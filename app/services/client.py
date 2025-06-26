from typing import AsyncGenerator
from app.dto.account import CreateAccountDto, PutAccountDto
from app.repositories.client import ClientRepository, GetClientsQueryDto
from app.dto.api import NotifyDto
from sqlalchemy.ext.asyncio import AsyncSession
import time


class ClientService:
    def __init__(self, client_repository: ClientRepository,
                 db_session: AsyncSession):
        self._client_repository = client_repository

    async def delete_client(self, id: int) -> bool:
        res = await self._client_repository.delete_client(id)
        return True if res else False

    async def get_clients(self, query: GetClientsQueryDto) -> tuple[dict, str]:
        clients, msg = await self._client_repository.get_clients(query)
        if not clients:
            return None, msg
        return {"clients": clients}, None 

    async def get_client_by_id(self, id: int) -> tuple[dict, str]:
        res = await self._client_repository.get_client_by_id(id)
        if not res:
            return {}, "客户端不存在"
        return res, ""

    # voip
    async def notify(self, client_id: str, data: NotifyDto) -> tuple[dict, str]:
        return await self._client_repository.notify(client_id, data)

    async def heartbeat(self, client_id: str) -> tuple[dict, str]:
        # 客户端是否存在
        if not await self.get_client_by_id(client_id):
            return {}, "客户端不存在"
        res = await self._client_repository.heartbeat(client_id)
        if res:
            return {"timestamp": time.time()}, None  
        return {}, "客户端不存在"

async def provide_client_service(
        client_repository: ClientRepository,
        db_session: AsyncSession) -> AsyncGenerator[ClientService, None]:
    yield ClientService(client_repository, db_session)
