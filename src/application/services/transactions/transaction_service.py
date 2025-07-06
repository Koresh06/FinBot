from dataclasses import dataclass

from src.domain.entities.monthly_balance import MonthlyBalance
from src.domain.entities.transaction import TransactionEntity
from src.domain.entities.user import UserEntity
from src.domain.repositories.monthly_balance_interface import IMonthlyBalanceRepository
from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.application.services.transactions.interface import ITransactionService


@dataclass
class TransactionServiceImpl(ITransactionService):

    transaction_repo: ITransactionRepository
    monthly_balance_repo: IMonthlyBalanceRepository

    async def add_transaction(self, monthly_balance: MonthlyBalance, transaction: TransactionEntity) -> TransactionEntity:
        await self.monthly_balance_repo.update(update_data=monthly_balance)
        return await self.transaction_repo.add(transaction)
