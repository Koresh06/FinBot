from abc import ABC, abstractmethod
from typing import Any

from src.domain.entities.monthly_balance import MonthlyBalance


class IMonthlyBalanceRepository(ABC):

    @abstractmethod
    def snapshot(self) -> Any:
        pass

    @abstractmethod
    def restore(self, state: Any) -> None:
        pass

    @abstractmethod
    async def get_current_by_item_id(self, tg_id: int, year: int, month: int) -> MonthlyBalance:
        pass

    @abstractmethod
    async def create(self, new_item: MonthlyBalance) -> MonthlyBalance:
        pass

    @abstractmethod
    async def update(self, update_data: MonthlyBalance) -> None:
        pass