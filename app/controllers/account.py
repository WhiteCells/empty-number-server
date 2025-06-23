from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.account import AccountService
from app.dto.account import CreateAccountDto, PutAccountDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger


class AccountController(Controller):

    @post(path="/account", status_code=HTTP_200_OK)
    async def create_account(self, data: CreateAccountDto, account_service: AccountService) -> Response:
        res, msg = await account_service.create_account(data)
        return jsonify(200, res, msg)

    @post(path="/account/upload_file", status_code=HTTP_200_OK)
    async def upload_file(self, request: Request) -> Response:
        return jsonify(200, "", "")

    @delete(path="/account/{id:int}", status_code=HTTP_200_OK)
    async def delete_account(self, id: int) -> Response:
        return jsonify(200, "", "")

    @put(path="/account/{id:int}", status_code=HTTP_200_OK)
    async def put_account(self, id: int, data: PutAccountDto) -> Response:
        return jsonify(200, "", "")

    @get(path="/account/{id:int}", status_code=HTTP_200_OK)
    async def get_account(self, id: int, account_service: AccountService) -> Response:
        data, msg = await account_service.get_account(id)
        return jsonify(200, "", "")

    @get(path="/accounts", status_code=HTTP_200_OK)
    async def get_accounts(self) -> Response:
        return jsonify(200, "", "")
