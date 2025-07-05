from dataclasses import dataclass, field

from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType
from src.domain.repositories.category_repo_interface import ICategoryRepository


@dataclass
class CategoryMemoryRepositoryImpl(ICategoryRepository):
    categories: list[CategoryEntity] = field(default_factory=list)
    counter: int = 1

    def snapshot(self):
        import copy
        return copy.deepcopy(self.categories)

    def restore(self, state):
        self.categories = state

    async def get_user_type_categories(self, user_id: int, type: OperationType) -> list[CategoryEntity]:
        return [cat for cat in self.categories if cat.user_id == user_id and cat.type == type]

    async def create(self, category: CategoryEntity) -> CategoryEntity:
        new_category = CategoryEntity(
            id=self.counter,
            name=category.name,
            user_id=category.user_id,
            type=OperationType(category.type)
        )
        self.counter += 1
        self.categories.append(new_category)
        return new_category
    
    async def get_all(self) -> list[CategoryEntity]:
        return self.categories


    async def find_duplicate_category(self, user_id: int, type: OperationType, name: str) -> CategoryEntity | None:
        for category in self.categories:
            if category.user_id == user_id and category.type == type and category.name == name:
                return category
        return None
