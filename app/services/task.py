from typing import AsyncGenerator
from app.repositories.task import TaskRepository
from app.dto.task import GetTasksQueryDto


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    async def get_tasks(self, query: GetTasksQueryDto) -> tuple[dict, str]:
        return await self._task_repository.get_tasks(query)

    async def get_task(self, id: int) -> tuple[dict, str]:
        return await self._task_repository.get_task(id)


async def provide_task_service(task_repository: TaskRepository) -> AsyncGenerator[TaskService, None]:
    yield TaskService(task_repository)
