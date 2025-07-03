from src.application.services.categories.exceptions import CategoryAlreadyExistsError
from src.application.services.categories.interface import ICategoryService
from src.domain.repositories.category_repo import ICategoryRepository
from src.domain.entities.category import CategoryEntity, DEFAULT_CATEGORIES


class CategoryServiceImpl(ICategoryService):
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    async def get_user_categories(self, user_id: int | None) -> list[CategoryEntity]:
        if user_id is None:
            raise ValueError("user_id не может быть None")
        return await self.category_repo.get_user_categories(user_id)

    async def create_category(self, category: CategoryEntity) -> CategoryEntity:
        existing = await self.category_repo.get_by_user_and_name(
            user_id=category.user_id,
            name=category.name,
        )
        if existing:
            raise CategoryAlreadyExistsError(f"Категория с именем '{category.name}' уже существует у пользователя {category.user_id}")

        return await self.category_repo.create(category)
    
    async def create_default_categories(self, user_id: int) -> None:
        for name in DEFAULT_CATEGORIES:
            category = CategoryEntity(name=name, user_id=user_id)
            await self.create_category(category)