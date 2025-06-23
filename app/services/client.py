from typing import AsyncGenerator
from app.dto.account import CreateAccountDto, PutAccountDto
from app.repositories.client import ClientRepository
from app.dto.api import NotifyDto


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self._client_repository = client_repository

    def notify(self, client_id: str, data: NotifyDto) -> tuple[dict, str]:
        return self._client_repository.notify(client_id, data)


async def provide_client_service(client_repository: ClientRepository) -> AsyncGenerator[ClientService, None]:
    yield ClientService(client_repository)
