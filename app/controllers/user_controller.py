from typing import List, Optional
from litestar import Controller, get, post, put, delete, Response, Router
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.exceptions import NotFoundException
from app.dto.user_dto import GetUserDTO
from app.services.user_service import UserService
from app.utils.jsonify import jsonify

from app.utils.logger import logger

class UserController(Controller):

    @get(path = "/{user_id:int}")
    async def get_user_by_id(self, user_id: int, user_service: UserService) -> GetUserDTO:
        user =  await user_service.get_user_by_id(user_id)
        logger.info("get user by id")
        return jsonify(200, user, "success")
