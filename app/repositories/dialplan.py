from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto, CreateDialplanResponseDto
from app.models.dialplan import Dialplan
from app.utils.logger import logger
import datetime
from app.models.dialplan import DialplanStatus
from app.models.task import Task


class DialplanRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

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
            return {
                "task_id": task.id,
                "dialplans": dialplans,
                "return_url": task.return_url
            }, None

        except Exception as e:
            await self._db_session.rollback()
            return None, f"创建任务失败 {e}"
    
    async def get_dialplan(self, client_id) -> tuple[dict, str]:
        pass


async def provide_dialplan_repository(db_session: AsyncSession) -> AsyncGenerator[DialplanRepository, None]:
    yield DialplanRepository(db_session)
