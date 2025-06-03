from app.dto.user_dto import GetUserDTO

class UserRepository:

    async def get_user_by_id(self, user_id: int) -> GetUserDTO:
        return GetUserDTO(id=user_id, username="user1", email="xxx@xxx.com")
