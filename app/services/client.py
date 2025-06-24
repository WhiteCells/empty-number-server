from typing import AsyncGenerator
from app.dto.account import CreateAccountDto, PutAccountDto
from app.repositories.client import ClientRepository
from app.dto.api import NotifyDto
from sqlalchemy.ext.asyncio import AsyncSession


class ClientService:
    def __init__(self, client_repository: ClientRepository,
                 db_session: AsyncSession):
        self._client_repository = client_repository

    async def delete_client(self, id: int) -> tuple[dict, str]:
        pass

    async def get_clients(self) -> tuple[dict, str]:
        pass

    async def get_client_by_id(self, id: int) -> tuple[dict, str]:
        pass

    # voip
    async def notify(self, client_id: str, data: NotifyDto) -> tuple[dict, str]:
        return await self._client_repository.notify(client_id, data)

    async def heartbeat(self, client_id: str) -> bool:
        return await self._client_repository.heartbeat(client_id)


async def provide_client_service(
        client_repository: ClientRepository,
        db_session: AsyncSession) -> AsyncGenerator[ClientService, None]:
    yield ClientService(client_repository, db_session)
