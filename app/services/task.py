from typing import AsyncGenerator
from app.repositories.task import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository


async def provide_task_service(task_repository: TaskRepository) -> AsyncGenerator[TaskService, None]:
    yield TaskService(task_repository)
