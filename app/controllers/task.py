from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.utils.jsonify import jsonify
from app.utils.logger import logger


class TaskController(Controller):

    @get(path="/task/{id:int}", status_code=HTTP_200_OK)
    async def get_task(self, id: int) -> Response:
        return jsonify(200, "", "")

    @get(path="/tasks", status_code=HTTP_200_OK)
    async def get_tasks(self) -> Response:
        return jsonify(200, "", "")
