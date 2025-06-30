from typing import AsyncGenerator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from redis.asyncio import Redis
from app.models.task import Task
from app.utils.logger import logger
from app.dto.task import GetTasksQueryDto, GetTasksResponseDto, GetTaskResponseDto


class TaskRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_tasks(self, query: GetTasksQueryDto) -> tuple[dict, str]:
        try:
            result = await self._db_session.execute(
                select(Task)
                .limit(query.size)
                .offset((query.page - 1) * query.size)
            )
            tasks = result.scalars().all()
            if not tasks:
                return None, "无任务"
            tasks_dict = [GetTasksResponseDto.model_validate(task) for task in tasks]
            return tasks_dict, "success"
        except Exception as e:
            logger.error(e)
            return None, "服务器错误"
        
    async def get_task(self, id: int) -> tuple[dict, str]:
        try:
            result = await self._db_session.execute(
                select(Task)
                .options(selectinload(Task.dialplans))
                .where(Task.id == id)
            )
            task = result.scalars().first()
            if not task:
                return None, "任务不存在"
            task_dto = GetTaskResponseDto.model_validate(task)
            return task_dto, None
        except Exception as e:
            logger.error(e)
            return None, "服务器错误"


async def provide_task_repository(db_session: AsyncSession) -> AsyncGenerator[TaskRepository, None]:
    yield TaskRepository(db_session)
