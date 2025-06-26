from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.client import ClientService
from app.services.dialplan import DialplanService
from app.services.account import AccountService
from app.dto.client import CreateClientDto, PutClientDto
from app.dto.account import PutAccountRegStatusDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger
from app.dto.api import NotifyDto
from app.dto.dialplan import DialplanStatusDto
from app.config import Config
import os


"""
面向客户端接口
"""
class ApiController(Controller):

    @post(path="/notify/{client_id:str}", status_code=HTTP_200_OK)
    async def notify(self, client_id: str, data: NotifyDto, client_service: ClientService) -> Response:
        res, msg = await client_service.notify(client_id, data)
        return jsonify(200, res, msg)

    @get(path="/account/{client_id:str}", status_code=HTTP_200_OK)
    async def get_account(self, client_id: str, account_service: AccountService) -> Response:
        """
        获取空闲或未使用的账号信息
        """
        res, msg = await account_service.get_free_account(client_id)
        return jsonify(200, res, msg)

    @put(path="/account/status/{client_id:str}", status_code=HTTP_200_OK)
    async def reg_status(self, client_id: str, data: PutAccountRegStatusDto, account_service: AccountService) -> Response:
        """
        """
        res = await account_service.update_reg_status(data)
        return jsonify(200, res, "")

    @get(path="/dialplan/{client_id:str}", status_code=HTTP_200_OK)
    async def get_dialplan(self, client_id: str, dialplan_service: DialplanService) -> Response:
        """
        获取指定客户端的分机分配的计划接口
        修改 dialplan 状态为处理中，设置 dialplan 的过期时间 2 分钟后
        """
        res, msg = await dialplan_service.get_dialplan(client_id)
        return jsonify(200, res, msg)

    @put(path="/dialplan/status/{client_id:str}", status_code=HTTP_200_OK)
    async def dialplan_status(self, client_id: str, data: DialplanStatusDto, dialplan_service: DialplanService) -> Response:
        """
        客户端拨号状态
        检查当前通话所在的任务的所有通话是否都完成，如果都完成，则更新任务状态
        """
        await dialplan_service.update_dialplan_status(client_id, data)
        return jsonify(200, "", "")
    
    @post(path="/heartbeat/{client_id:str}", status_code=HTTP_200_OK)
    async def heartbeat(self, client_id: str, client_service: ClientService) -> Response:
        """
        心跳接口
        更新客户端在 redis 中的状态
        """
        res = await client_service.heartbeat(client_id)
        return jsonify(200, res, "")
    
    @post(path="/dial_wav/{client_id:str}", status_code=HTTP_200_OK)
    async def dial_wav(self, client_id: str, request: Request, dialplan_service: DialplanService) -> Response:
        """
        通话前音频文件接收接口
        """
        filename = request.headers.get("filename")
        if not filename:
            return jsonify(400, "", "filename is required")
        
        # 按下划线拆分文件名，找到 phone，根据 phone 找到 task ID，创建 task ID 目录
        phone = filename.split("_")[0]

        task_id = await dialplan_service.get_task_id(client_id, phone)
        if not task_id:
            return jsonify(400, "", "task_id is not found")

        os.makedirs(f"{Config.UPLOADS_DIR}/{task_id}", exist_ok=True)

        body = await request.body()
        file_path = os.path.join(Config.UPLOADS_DIR, str(task_id), filename)

        with open(file_path, "wb") as f:
            f.write(body)

        return jsonify(200, "", "")
