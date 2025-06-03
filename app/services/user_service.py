from typing import Optional, List
from app.dto.user_dto import GetUserDTO
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: int) -> GetUserDTO:
        user = await self.user_repository.get_user_by_id(user_id)
        return GetUserDTO.model_validate(user.model_dump()) if user else None
