from typing import AsyncGenerator
from sqlalchemy import select, delete, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.account import CreateAccountDto, PutAccountDto, CreateAccountResponseDto, GetAccountResponseDto
from app.models.account import Account, AccountStatus
from app.utils.logger import logger
from app.utils.redisclient.cluster_client import get_redis_cluster_client
from datetime import datetime, timedelta


class AccountRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._cluster_client = get_redis_cluster_client()

    async def create_account(self, data: CreateAccountDto) -> tuple[dict, str]:
        accounts = []
        try:
            now = datetime.now()
            expired_at = now + timedelta(seconds=120)
            async with self._db_session.begin():
                for acc in data.account:
                    account = Account(
                        host=acc.host,
                        name=acc.name,
                        pwd=acc.pwd,
                        expired_at=expired_at
                    )
                    self._db_session.add(account)
                    accounts.append(CreateAccountResponseDto.model_validate(account))
            return {"accounts": accounts}, None
        except Exception as e:
            logger.error(e)
            return None, f"创建账户失败 {e}"
        
    async def delete_account(self, id: int) -> bool:
        result = await self._db_session.execute(
            delete(Account).where(Account.id == id)
        )
        return result.rowcount > 0

    async def update_account_status(self, id: int, _status: str) -> bool:
        stmt = (
            update(Account)
            .where(Account.id == id)
            .values(
                status = _status,
                expired_at = datetime.now() + timedelta(seconds=120),
            )
        )
        result = await self._db_session.execute(stmt)
        if result.rowcount == 0:
            return False
        return True
        
    async def get_free_account(self, count: int) -> tuple[dict, str]:
        """
        获取账号状态为空闲的账户
        """
        try:
            # 获取未占用或者过期的账户
            now = datetime.now()
            result = await self._db_session.execute(
                select(Account)
                .where(
                    or_(
                        Account.status == AccountStatus.Free,
                        and_(
                            Account.status == AccountStatus.Used,
                            Account.expired_at != None,
                            Account.expired_at < now,
                        )
                    )
                )
                .limit(count)
            )
            accounts = result.scalars().all()
            if not accounts:
                return None, "无空闲账户"
            # 更新账号状态为占用，更新账号过期时间
            for account in accounts:
                account.status = AccountStatus.Used

            accounts_dto = [GetAccountResponseDto.model_validate(acc) for acc in accounts]
            return {
                "accounts": accounts_dto,
            }, None
        except Exception as e:
            logger.error(e)
            return None, f"获取空闲账户失败 {e}"
        
    async def get_account(self, id: int) -> tuple[dict, str]:
        try:
            result = await self._db_session.execute(
                select(Account).where(Account.id == id)
            )
            account = result.scalar_one_or_none()
            if not account:
                return None, "账户不存在"
            account = GetAccountResponseDto.model_validate(account)
            return account, None
        except Exception as e:
            logger.error(e)
            return None, f"获取账户失败 {e}"
        

async def provide_account_repository(db_session: AsyncSession) -> AsyncGenerator[AccountRepository, None]:
    yield AccountRepository(db_session)
