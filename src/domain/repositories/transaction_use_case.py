from abc import ABC, abstractmethod
from src.domain.entities.transaction import TransactionEntity


class ITransactionRepository(ABC):

    @abstractmethod
    async def add(self, transaction: TransactionEntity) -> TransactionEntity:
        pass