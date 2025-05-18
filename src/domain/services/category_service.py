from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.category import CategoryEntity


class ICategoryService(ABC):

    @abstractmethod
    async def get_user_categories(self, user_id: Optional[int]) -> list[CategoryEntity]:
        ...

    @abstractmethod
    async def create_category(self, category: CategoryEntity) -> CategoryEntity:
        ...

    @abstractmethod
    async def create_default_categories(self, user_id: int) -> CategoryEntity:
        ...