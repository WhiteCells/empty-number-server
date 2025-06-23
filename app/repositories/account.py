from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.account import CreateAccountDto, PutAccountDto, CreateAccountResponseDto
from app.models.account import Account
from app.utils.logger import logger


class AccountRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create_account(self, data: CreateAccountDto) -> tuple[dict, str]:
        accounts = []
        try:
            async with self._db_session.begin():
                for acc in data.account:
                    account = Account(
                        host=acc.host,
                        name=acc.name,
                        pwd=acc.pwd,
                    )
                    self._db_session.add(account)
                    accounts.append(CreateAccountResponseDto.model_validate(account))
            return {"accounts": accounts}, None
        except Exception as e:
            logger.error(e)
            return None, f"创建账户失败 {e}"


async def provide_account_repository(db_session: AsyncSession) -> AsyncGenerator[AccountRepository, None]:
    yield AccountRepository(db_session)
