from typing import Optional
from src.domain.services.user_service_intarface import IUserService
from src.domain.entities.user import UserEntity
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.application.services.users.exceptions import UserAlreadyExistsError, UserNotFountError


class UserServiceImpl(IUserService):
    def __init__(self, repository: IUserRepository):
        self._repo = repository
        
    async def register_user(self, user: UserEntity) -> UserEntity:
        existing_user = await self._repo.get_by_tg_id(user.tg_id)
        if existing_user is not None:
            raise UserAlreadyExistsError("Пользователь с таким tg_id уже существует")

        return await self._repo.register(user)
    
    async def get_user_by_tg_id(self, tg_id: int) -> UserEntity:
        user = await self._repo.get_by_tg_id(tg_id)
        if not user:
            raise UserNotFountError("Пользователя с таким tg_id не существует")
        return user
    
    async def update_user_settings(self, tg_id: int, currency: Optional[str] = None) -> UserEntity:
        user = await self.get_user_by_tg_id(tg_id)
        if currency:
            user.currency = currency
        return await self._repo.update(user)
    
    async def set_monthly_budget(self, tg_id: int, budget: float) -> UserEntity:
        user = await self.get_user_by_tg_id(tg_id)
        user.monthly_budget = budget
        return await self._repo.update(user)