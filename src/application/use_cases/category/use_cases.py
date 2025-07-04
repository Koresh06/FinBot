from dataclasses import dataclass

from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType
from src.application.services.users.interface import IUserService
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity
from src.application.services.categories.interface import ICategoryService


@dataclass
class GetCategoriesOfUserUseCase(UseCaseMultipleEntities[CategoryEntity]):
        
    category_service: ICategoryService
    user_service: IUserService

    async def execute(self, tg_id: int, type: OperationType) -> list[CategoryEntity]:
        user = await self.user_service.get_user_by_tg_id(tg_id)
        if user is None:
            raise ValueError(f"Пользователь с tg_id={tg_id} не найден")
        return await self.category_service.get_user_type_categories(user.id, type)

@dataclass
class CreateCategoryUserUseCase(UseCaseOneEntity[CategoryEntity]):

    category_service: ICategoryService
    user_service: IUserService

    async def execute(self, tg_id: int, type: OperationType, name: str) -> None:
        user = await self.user_service.get_user_by_tg_id(tg_id)
        if user is None:
            raise ValueError(f"Пользователь с tg_id={tg_id} не найден")
        if user.id is None:
            raise ValueError("ID пользователя не может быть None")
    
        await self.category_service.create_category(
            CategoryEntity(
                name=name,
                user_id=user.id,
                type=type,
            )
        )

