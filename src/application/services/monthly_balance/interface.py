from abc import ABC, abstractmethod

from src.domain.entities.monthly_balance import MonthlyBalance


class IMonthlyBalanceService(ABC):

    @abstractmethod
    async def get_by_user_id(self, tg_id: int) -> MonthlyBalance:
        pass
