from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.models.task import Task
from app.utils.logger import logger


class TaskRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    # async def create_task(self, data: dict) -> dict:
    #     task = Task(**data)
    #     self._db_session.add(task)
    #     await self._db_session.commit()
    #     return task.to_dict()


async def provide_task_repository(db_session: AsyncSession) -> AsyncGenerator[TaskRepository, None]:
    yield TaskRepository(db_session)
