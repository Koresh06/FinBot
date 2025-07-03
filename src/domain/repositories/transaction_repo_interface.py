from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities.transaction import TransactionEntity


class ITransactionRepository(ABC):

    @abstractmethod
    def snapshot(self) -> Any:
        pass

    @abstractmethod
    def restore(self, state: Any) -> None:
        pass

    @abstractmethod
    async def add(self, transaction: TransactionEntity) -> TransactionEntity:
        pass