from typing import AsyncGenerator
from app.repositories.dialplan import DialplanRepository
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto


class DialplanService:
    def __init__(self, dialplan_repository: DialplanRepository):
        self._dialplan_repository = dialplan_repository

    async def create_dialplan(self, data: CreateDialplanDto) -> tuple[dict, str]:
        return await self._dialplan_repository.create_dialplan(data)

    async def get_dialplan(self, client_id) -> tuple[dict, str]:
        return await self._dialplan_repository.get_dialplan(client_id)


async def provide_dialplan_service(dialplan_repository: DialplanRepository) -> AsyncGenerator[DialplanService, None]:
    yield DialplanService(dialplan_repository)
