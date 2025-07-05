from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType


class ICategoryService(ABC):

    @abstractmethod
    async def get_user_type_categories(self, user_id: int | None, type: OperationType) -> list[CategoryEntity]:
        ...

    @abstractmethod
    async def create_category(self, category: CategoryEntity) -> CategoryEntity:
        ...

    @abstractmethod
    async def create_default_categories(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def get_all_categories(self) -> list[CategoryEntity]:
        pass