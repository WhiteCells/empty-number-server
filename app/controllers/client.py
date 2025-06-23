from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.client import ClientService
from app.dto.client import CreateClientDto, PutClientDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger


class ClientController(Controller):

    @post(path="/client", status_code=HTTP_200_OK)
    async def create_client(self, data: CreateClientDto) -> Response:
        return jsonify(200, "", "")

    @post(path="/client/upload_file", status_code=HTTP_200_OK)
    async def upload_file(self, request: Request) -> Response:
        return jsonify(200, "", "")

    @delete(path="/client/{id:int}", status_code=HTTP_200_OK)
    async def delete_client(self, id: int) -> Response:
        return jsonify(200, "", "")

    @put(path="/client/{id:int}", status_code=HTTP_200_OK)
    async def put_client(self, id: int, data: PutClientDto) -> Response:
        return jsonify(200, "", "")

    @get(path="/clients", status_code=HTTP_200_OK)
    async def get_clients(self) -> Response:
        return jsonify(200, "", "")
