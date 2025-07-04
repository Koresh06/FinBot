from dataclasses import dataclass

from src.domain.value_objects.currency_enum import CurrencyEnum
from src.application.services.users.interface import IUserService
from src.domain.entities.user import UserEntity
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.application.services.users.exceptions import UserAlreadyExistsError, UserNotFountError


@dataclass
class UserServiceImpl(IUserService):
        
    user_repo: IUserRepository
        
    async def register_user(self, user: UserEntity) -> UserEntity:
        existing_user = await self.user_repo.get_by_tg_id(user.tg_id)
        if existing_user is not None:
            raise UserAlreadyExistsError("Пользователь с таким tg_id уже существует")

        return await self.user_repo.register(user)
    

    async def get_user_by_tg_id(self, tg_id: int) -> UserEntity | None:
        user = await self.user_repo.get_by_tg_id(tg_id)
        if not user:
            raise UserNotFountError("Пользователя с таким tg_id не существует")
        return user


        

    # async def update_user_settings(self, tg_id: int, update_data: dict) -> None:
    #     user = await self.get_user_by_tg_id(tg_id)
    #     if user is None:
    #         raise ValueError(f"Пользователь с tg_id={tg_id} не найден")

    #     await self.user_repo.update(user.id, update_data)