from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.category import CategoryEntity


class ICategoryRepository(ABC):

    @abstractmethod
    async def get_user_categories(self, user_id: int) -> list[CategoryEntity]:
        pass

    @abstractmethod
    async def create(self, category: CategoryEntity) -> CategoryEntity:
        pass

    @abstractmethod
    async def get_by_user_and_name(self, user_id: int, name: str) -> Optional[CategoryEntity]:
        pass
