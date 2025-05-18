from typing import Optional
from src.domain.entities.category import CategoryEntity
from src.domain.repositories.category_repo import ICategoryRepository


class CategoryMemoryRepositoryImpl(ICategoryRepository):
    def __init__(self):
        self.categories_by_user: dict[int, list[CategoryEntity]] = {}
        self.counter = 1

    async def get_user_categories(self, user_id: int) -> list[CategoryEntity]:
        return self.categories_by_user.get(user_id, [])

    async def create(self, category: CategoryEntity) -> CategoryEntity:
        new_category = CategoryEntity(
            id=self.counter,
            name=category.name,
            user_id=category.user_id
        )
        self.counter += 1

        if category.user_id not in self.categories_by_user:
            self.categories_by_user[category.user_id] = []

        self.categories_by_user[category.user_id].append(new_category)
        return new_category

    async def get_by_user_and_name(self, user_id: int, name: str) -> Optional[CategoryEntity]:
        for category in self.categories_by_user.get(user_id, []):
            if category.name == name:
                return category
        return None

