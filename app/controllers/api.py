from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.client import ClientService
from app.services.dialplan import DialplanService
from app.services.account import AccountService
from app.dto.client import CreateClientDto, PutClientDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger
from app.dto.api import NotifyDto

"""
面向客户端接口
"""
class ApiController(Controller):

    @post(path="/notify/{client_id:str}")
    async def notify(self, client_id: str, data: NotifyDto, client_service: ClientService) -> Response:
        """
        """
        res, msg = await client_service.notify(client_id, data)
        return jsonify(200, res, msg)

    @get("/dialplan/{client_id:str}")
    async def get_dialplan(self, client_id: str, dialplan_service: DialplanService) -> Response:
        """
        获取指定客户端的分机分配的计划接口
        """
        dialplan_service.get_dialplan(client_id)
        return jsonify(200, "", "")

    @get("/account/{client_id:str}")
    async def get_account(self, client_id: str, account_service: AccountService) -> Response:
        """
        获取客户端对应的账号信息
        """
        # account_service
        return jsonify(200, "", "")

    @post("/account/reg_status/{client_id:str}")
    async def reg_status(self, client_id: str) -> Response:
        """
        客户端注册账号状态
        """
        return jsonify(200, "", "")

    @post("/heartbeat/{client_id:str}")
    async def heartbeat(self, client_id: str) -> Response:
        """
        心跳接口
        更新客户端在 redis 中的状态
        """
        return jsonify(200, "", "")
    
    @post("/dialplan/status/{client_id:str}")
    async def dialplan_status(self, client_id: str) -> Response:
        """
        客户端拨号状态
        更新客户端在数据库中的状态
        """
        return jsonify(200, "", "")
    
    @post("/dialplan/empty_res")
    async def dialplan_empty_res(self, request: Request) -> Response:
        """
        空号结果(回调)
        """
        return jsonify(200, "", "")