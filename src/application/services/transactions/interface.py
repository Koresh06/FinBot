from abc import ABC, abstractmethod

from src.domain.entities.monthly_balance import MonthlyBalance
from src.domain.entities.transaction import TransactionEntity


class ITransactionService(ABC):

    @abstractmethod
    async def add_transaction(self, monthly_balance: MonthlyBalance, transaction: TransactionEntity) -> TransactionEntity:
        pass
