from abc import ABC

from src.domain.entities.user import UserEntity


class IUserService(ABC):

    async def register_user(self, user: UserEntity) -> UserEntity:
        ...

    async def get_user_by_tg_id(self, tg_id: int) -> UserEntity | None:
        ...

    async def update_user_settings(self, tg_id: int, currency: str | None = None) -> None:
        ...

    async def set_monthly_budget(self, tg_id: int, budget: float) -> None:
        ...