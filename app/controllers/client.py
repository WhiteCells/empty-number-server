from litestar import Controller, get, post, delete, put, Response, Request
from litestar.status_codes import HTTP_200_OK
from app.services.client import ClientService
from app.dto.client import CreateClientDto, PutClientDto, GetClientsQueryDto
from app.utils.jsonify import jsonify
from app.utils.logger import logger


class ClientController(Controller):

    @delete(path="/client/{id:int}", status_code=HTTP_200_OK)
    async def delete_client(self, id: int, client_service: ClientService) -> Response:
        await client_service.delete_client(id)
        return jsonify(200, "", "")
    
    @get(path="/client/{id:int}", status_code=HTTP_200_OK)
    async def get_client_by_id(self, id: int, client_service: ClientService) -> Response:
        client, msg = await client_service.get_client_by_id(id)
        return jsonify(200, client, msg)

    # /clients?page=1&size=10
    @get(path="/clients", status_code=HTTP_200_OK)
    async def get_clients(self, query: GetClientsQueryDto, client_service: ClientService) -> Response:
        clients, msg = await client_service.get_clients(query)
        return jsonify(200, clients, msg)
