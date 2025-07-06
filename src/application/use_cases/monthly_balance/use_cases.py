from dataclasses import dataclass

from src.application.use_cases.intarface import UseCaseOneEntity
from src.domain.entities.monthly_balance import MonthlyBalance
from src.application.services.monthly_balance.interface import IMonthlyBalanceService




@dataclass
class GetMonthlyBalanceUseCase(UseCaseOneEntity[MonthlyBalance | None]):

    monthly_balance_service: IMonthlyBalanceService

    async def execute(self, tg_id: int) -> MonthlyBalance | None:
        return await self.monthly_balance_service.get_by_user_id(tg_id)