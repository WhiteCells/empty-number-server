from typing import AsyncGenerator
from app.dto.account import CreateAccountDto, PutAccountRegStatusDto
from app.repositories.account import AccountRepository
from app.repositories.client import ClientRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AccountService:
    def __init__(self, 
                 account_repository: AccountRepository,
                 client_respository: ClientRepository,
                 db_session: AsyncSession):
        self._account_repository = account_repository
        self._client_respository = client_respository
        self._db_session = db_session

    async def create_account(self, data: CreateAccountDto) -> tuple[dict, str]:
        return await self._account_repository.create_account(data)
    
    async def delete_account(self, id: int) -> tuple[dict, str]:
        async with self._db_session.begin():
            return await self._account_repository.delete_account(id)
    
    async def get_free_account(self, client_id: str) -> tuple[dict, str]:
        # 查询对应客户端是否存在，不存在直接获取失败，存在则获取客户端线程数
        async with self._db_session.begin():
            client = await self._client_respository.get_client_by_uuid(client_id)
            if not client:
                return None, "客户端不存在"
            return await self._account_repository.get_free_account(client["threads_num"])

    async def update_reg_status(self, data: PutAccountRegStatusDto) -> dict:
        async with self._db_session.begin():
            res = await self._account_repository.update_account_status(data.account_id, data.status)
            if res:
                return {"message": "更新成功"}
            return {"message": "更新失败"}

    async def get_account(self, id: int) -> tuple[dict, str]:
        async with self._db_session.begin():
            return await self._account_repository.get_account(id)

async def provide_account_service(
        account_repository: AccountRepository,
        client_repository: ClientRepository,
        db_session: AsyncSession) -> AsyncGenerator[AccountService, None]:
    yield AccountService(account_repository, client_repository, db_session)
