from dataclasses import dataclass

from src.application.uow.interfase import AbstractUnitOfWork
from src.domain.entities.transaction import TransactionEntity
from src.application.services.transactions.interface import ITransactionService
from src.application.use_cases.intarface import UseCaseOneEntity
from src.application.services.monthly_balance.interface import IMonthlyBalanceService


@dataclass
class AddTransactionUseCase(UseCaseOneEntity[TransactionEntity]):
    transac_service: ITransactionService
    monthly_balance_service: IMonthlyBalanceService
    uow: AbstractUnitOfWork

    async def execute(self, tg_id: int, data: dict) -> None:
        async with self.uow:
            monthly_balance = await self.monthly_balance_service.get_by_user_id(tg_id)

            transaction = TransactionEntity(
                tg_id=monthly_balance.tg_id,
                category_id=data["category"],
                amount=data["total_sum"],
                type=data["type"],
                comment=data["comment"],
            )

            monthly_balance.apply_transaction(transaction)

            await self.transac_service.add_transaction(monthly_balance, transaction)