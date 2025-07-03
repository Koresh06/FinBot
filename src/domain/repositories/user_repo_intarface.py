from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def snapshot(self) -> Any:
        pass

    @abstractmethod
    def restore(self, state: Any) -> None:
        pass

    @abstractmethod
    async def register(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> UserEntity | None:
        pass

    @abstractmethod
    async def update(self, user_update: UserEntity) -> None:
        pass
