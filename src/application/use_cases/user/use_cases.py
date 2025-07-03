from dataclasses import asdict
from src.application.dto.user import UserDTO
from src.application.services.categories.interface import ICategoryService
from src.application.use_cases.intarface import UseCaseOneEntity
from src.domain.entities.user import UserEntity
from src.application.services.users.interface import IUserService


class RegisterUserUseCase(UseCaseOneEntity[UserEntity]):
    def __init__(
        self,
        user_service: IUserService,
        category_service: ICategoryService,
    ):
        self.user_service = user_service
        self.category_service = category_service

    async def execute(self, user: UserEntity) -> UserEntity:

        user = await self.user_service.register_user(user)

        if not user.id:
            raise ValueError("User ID is None after registration")

        await self.category_service.create_default_categories(user.id)

        return user


class GetUserByTgIdUseCase(UseCaseOneEntity[UserEntity | None]):
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    async def execute(self, tg_id: int) -> UserEntity | None:
        return await self.user_service.get_user_by_tg_id(tg_id)


# class UpdateUserSettingsUseCase(UseCaseOneEntity[None]):

#     def __init__(self, user_service: IUserService):
#         self.user_service = user_service

#     async def execute(self, tg_id: int, currency: str) -> None:
#         await self.user_service.update_user_settings(
#             tg_id=tg_id,
#             currency=currency,
#         )


# class SetUserMonthlyBudgetUseCase(UseCaseOneEntity[None]):

#     def __init__(self, user_service: IUserService):
#         self.user_service = user_service

#     async def execute(self, tg_id: int, budget: float) -> None:
#         await self.user_service.set_monthly_budget(
#             tg_id=tg_id,
#             budget=budget,
#         )

