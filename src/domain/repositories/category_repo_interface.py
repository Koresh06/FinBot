from abc import ABC, abstractmethod
from typing import Any, Optional
from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType


class ICategoryRepository(ABC):

    @abstractmethod
    def snapshot(self) -> Any:
        pass

    @abstractmethod
    def restore(self, state: Any) -> None:
        pass

    @abstractmethod
    async def get_user_type_categories(self, user_id: int, type: OperationType) -> list[CategoryEntity]:
        pass

    @abstractmethod
    async def create(self, category: CategoryEntity) -> CategoryEntity:
        pass

    @abstractmethod
    async def get_all(self) -> list[CategoryEntity]:
        pass

    @abstractmethod
    async def find_duplicate_category(self, user_id: int, type: OperationType, name: str) -> CategoryEntity | None:
        pass
