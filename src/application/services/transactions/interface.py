from abc import ABC, abstractmethod

from src.domain.entities.transaction import TransactionEntity


class ITransactionService(ABC):

    @abstractmethod
    async def add_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        pass
