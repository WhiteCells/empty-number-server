from typing import AsyncGenerator
from app.dto.account import CreateAccountDto, PutAccountDto
from app.repositories.account import AccountRepository


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

    def create_account(self, data: CreateAccountDto) -> tuple[dict, str]:
        return self._account_repository.create_account(data)

async def provide_account_service(account_repository: AccountRepository) -> AsyncGenerator[AccountService, None]:
    yield AccountService(account_repository)
