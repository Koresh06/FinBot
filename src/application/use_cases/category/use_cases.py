from src.domain.entities.category import CategoryEntity
from src.application.services.users.interface import IUserService
from src.application.use_cases.base_use_case import BaseUseCase
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity
from src.application.services.categories.interface import ICategoryService


class GetCategoriesOfUserUseCase(UseCaseMultipleEntities[CategoryEntity], BaseUseCase):
    def __init__(
        self,
        category_service: ICategoryService,
        user_service: IUserService,
    ):
        self.category_service = category_service
        self.user_service = user_service

    async def execute(self, tg_id: int) -> list[CategoryEntity]:
        user = await self.user_service.get_user_by_tg_id(tg_id)
        if user is None:
            raise ValueError(f"Пользователь с tg_id={tg_id} не найден")
        return await self.category_service.get_user_categories(user.id)


class CreateCategoryUserUseCase(UseCaseOneEntity[CategoryEntity], BaseUseCase):
    def __init__(
        self,
        category_service: ICategoryService,
        user_service: IUserService,
    ):
        self.category_service = category_service
        self.user_service = user_service

    async def execute(self, tg_id: int, name: str) -> None:
        user = await self.user_service.get_user_by_tg_id(tg_id)
        if user is None:
            raise ValueError(f"Пользователь с tg_id={tg_id} не найден")
        if user.id is None:
            raise ValueError("ID пользователя не может быть None")
    
        await self.category_service.create_category(
            CategoryEntity(
                name=name,
                user_id=user.id,
            )
        )

