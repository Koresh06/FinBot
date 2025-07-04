from dataclasses import dataclass

from src.domain.repositories.category_repo_interface import ICategoryRepository
from src.domain.entities.category import CategoryEntity, DEFAULT_CATEGORIES
from src.domain.value_objects.operetion_type_enum import OperationType
from src.application.services.categories.exceptions import CategoryAlreadyExistsError
from src.application.services.categories.interface import ICategoryService


@dataclass
class CategoryServiceImpl(ICategoryService):

    category_repo: ICategoryRepository

    async def get_user_type_categories(self, user_id: int | None, type: OperationType) -> list[CategoryEntity]:
        if user_id is None:
            raise ValueError("user_id не может быть None")
        return await self.category_repo.get_user_type_categories(user_id, type)

    async def create_category(self, category: CategoryEntity) -> CategoryEntity:
        existing = await self.category_repo.find_duplicate_category(
            user_id=category.user_id,
            name=category.name,
            type=category.type,
        )
        if existing:
            raise CategoryAlreadyExistsError(f"Категория с именем '{category.name}' и типом '{category.type}' уже существует у пользователя {category.user_id}")

        return await self.category_repo.create(category)

    async def create_default_categories(self, user_id: int) -> None:
        for cat_type, names in DEFAULT_CATEGORIES.items():
            for name in names:
                category = CategoryEntity(
                    name=name,
                    user_id=user_id,
                    type=OperationType(cat_type),
                )
                await self.create_category(category)
