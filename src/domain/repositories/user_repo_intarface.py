from abc import ABC
from src.domain.entities.user import UserEntity


class IUserRepository(ABC):

    async def register(self, user: UserEntity) -> UserEntity:
        pass

    async def get_by_tg_id(self, tg_id: int) -> UserEntity | None:
        pass

    async def update(self, user: UserEntity) -> UserEntity:
        pass