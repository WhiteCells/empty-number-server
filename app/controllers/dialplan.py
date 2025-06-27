from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.dialplan import DialplanService
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger
from litestar.exceptions import HTTPException
from litestar.datastructures import UploadFile


class DialplanController(Controller):

    @post(path="/dialplan", status_code=HTTP_200_OK)
    async def create_dialpaln(self, data: CreateDialplanDto, dialplan_service: DialplanService) -> Response:
        """
        {
            "phone": [
                "18822223333",
                "18844445555"
            ],
            "return_url": "http://127.0.0.1:5001"
        }
        """
        res, msg = await dialplan_service.create_dialplan(data)

        return jsonify(200, res, msg)

    @post(path="/dialplan/upload_file", status_code=HTTP_200_OK)
    async def upload_file(self, request: Request) -> Response:
        form = await request.form()
        if "file" not in form:
            raise HTTPException(status_code=400, detail="请上传文件")
        file = form.get("file")
        if not isinstance(file, UploadFile):
            raise HTTPException(status_code=400, detail="请上传文件")
        content = await file.read()
        # todo
        return jsonify(200, content, "上传成功")
    
    @delete(path="/dialplan/{id:int}", status_code=HTTP_200_OK)
    async def delete_dialplan(self, id: int) -> Response:
        return jsonify(200, "", "")

    @put(path="/dialplan/{id:int}", status_code=HTTP_200_OK)
    async def put_dialplan(self, id: int, data: PutDialplanDto) -> Response:
        return jsonify(200, "", "")

    @get(path="/dialplan/{id:int}", status_code=HTTP_200_OK)
    async def get_dialplan(id: int) -> Response:
        return jsonify(200, "", "")

    @get(path="/dialplans", status_code=HTTP_200_OK)
    async def get_dialplans(self) -> Response:
        return jsonify(200, "", "")