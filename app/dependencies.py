from typing import AsyncGenerator
from litestar.di import Provide
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

async def provide_user_repository() -> AsyncGenerator[UserRepository, None]:
    yield UserRepository()

async def provide_user_service(user_repository: UserRepository) -> AsyncGenerator[UserService, None]:
    yield UserService(user_repository)

dependencies = {
    "user_repository": Provide(provide_user_repository),
    "user_service": Provide(provide_user_service),
}
