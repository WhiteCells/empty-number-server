from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.utils.jsonify import jsonify
from app.utils.logger import logger
from app.services.task import TaskService
from app.dto.task import GetTasksQueryDto


class TaskController(Controller):

    @get(path="/task/{id:int}", status_code=HTTP_200_OK)
    async def get_task(self, id: int, task_service: TaskService) -> Response:
        res, msg = await task_service.get_task(id)
        return jsonify(200, res, msg)

    @get(path="/tasks", status_code=HTTP_200_OK)
    async def get_tasks(self, query :GetTasksQueryDto, task_service: TaskService) -> Response:
        res, msg = await task_service.get_tasks(query)
        return jsonify(200, res, msg)
