from typing import AsyncGenerator
from app.repositories.dialplan import DialplanRepository
from app.repositories.client import ClientRepository
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto
from app.dto.dialplan import CreateDialplanResponseDto
from sqlalchemy.ext.asyncio import AsyncSession


class DialplanService:
    def __init__(self, 
                 dialplan_repository: DialplanRepository, 
                 client_repository: ClientRepository,
                 db_session: AsyncSession):
        self._dialplan_repository = dialplan_repository
        self._client_repository = client_repository
        self._db_session = db_session

    async def create_dialplan(self, data: CreateDialplanDto) -> tuple[dict, str]:
        return await self._dialplan_repository.create_dialplan(data)

    async def get_dialplan(self, client_id) -> tuple[dict, str]:
        # 判断 client_id 是否存在
        client =  await self._client_repository.get_client_by_uuid(client_id)
        if not client:
            return None, "client 不存在"
        return await self._dialplan_repository.get_dialplan(client["threads_num"])
    
    async def update_dialplan_status(self, client_id: str, data: PutDialplanDto) -> tuple[dict, str]:
        async with self._db_session.begin():
            return await self._dialplan_repository.update_dialplan_status(data.account_id, data.phone, data.status)
        return {}, None


async def provide_dialplan_service(
        dialplan_repository: DialplanRepository,
        client_repository: ClientRepository,
        db_session: AsyncSession) -> AsyncGenerator[DialplanService, None]:
    yield DialplanService(dialplan_repository, client_repository, db_session)
