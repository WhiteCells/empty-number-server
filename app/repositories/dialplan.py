import datetime
from typing import AsyncGenerator
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto, CreateDialplanResponseDto
from app.models.dialplan import Dialplan, DialplanStatus
from app.models.account import Account, AccountStatus
from app.models.task import Task
from app.utils.dialplan_queue import get_dialplan_queue
from app.utils.logger import logger


class DialplanRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._dialplan_queue = get_dialplan_queue()

    async def create_dialplan(self, data: CreateDialplanDto) -> tuple[dict, str]:
        task = None
        dialplans = []

        try:
            async with self._db_session.begin():
                # 创建 task 实例
                task = Task(
                    return_url=data.return_url,
                )
                self._db_session.add(task)
                await self._db_session.flush()
                await self._db_session.refresh(task)
                # 创建 dialplan 实例
                for phone in data.phone:
                    dialplan = Dialplan(
                        phone=phone,
                        task_id=task.id,
                    )
                    self._db_session.add(dialplan)
                    await self._db_session.flush()
                    dialplans.append(CreateDialplanResponseDto.model_validate(dialplan))
                    # phones.append(phone)
                    # 添加进 dialplan 队列
                    # self._dialplan_queue.put("dialplan", phone)
            return {
                "task_id": task.id,
                "dialplans": dialplans,
                "return_url": task.return_url
            }, None

        except Exception as e:
            await self._db_session.rollback()
            return None, f"创建任务失败 {e}"
    
    async def get_dialplan(self, threads_num) -> tuple[dict, str]:
        # 从队列中取出 threads_num 个 dialplan
        dialplan = self._dialplan_queue.get("dialplan", threads_num)
        return {"dialplans": dialplan}, None

    async def update_dialplan_status(self, phone: str, _status: str):
        stmt = (
            update(Dialplan)
            .where(Dialplan.phone == phone)
            .values(status = _status)
        )
        await self._db_session.execute(stmt)

    async def get_task_id(self, client_id: str, phone: str) -> int:
        result = await self._db_session.execute(
            select(Dialplan)
            .where(Dialplan.phone == phone)
        )
        dialplan = result.scalar_one_or_none()
        if not dialplan:
            return None
        return dialplan.task_id


async def provide_dialplan_repository(db_session: AsyncSession) -> AsyncGenerator[DialplanRepository, None]:
    yield DialplanRepository(db_session)
