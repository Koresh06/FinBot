from dataclasses import dataclass
from datetime import datetime

from src.application.services.monthly_balance.interface import IMonthlyBalanceService
from src.domain.entities.monthly_balance import MonthlyBalance
from src.domain.repositories.monthly_balance_interface import IMonthlyBalanceRepository


@dataclass
class MonthlyBalanceServiceImpl(IMonthlyBalanceService):

    monthly_balance_repo: IMonthlyBalanceRepository

    async def get_by_user_id(self, tg_id: int) -> MonthlyBalance:
        now = datetime.now()
        year, month = now.year, now.month

        current = await self.monthly_balance_repo.get_current_by_item_id(
            tg_id=tg_id,
            year=year,
            month=month,
        )
        if current:
            return current
        
        new_item  = MonthlyBalance(
            tg_id=tg_id,
            year=year,
            month=month,
        )
        return await self.monthly_balance_repo.create(new_item)

