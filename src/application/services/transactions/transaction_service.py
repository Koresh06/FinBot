from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.category_repo import ICategoryRepository
from src.domain.repositories.transaction_use_case import ITransactionRepository
from src.domain.services.transaction_service import ITransactionService


class TransactionServiceImpl(ITransactionService):

    def __init__(
        self,
        repository: ITransactionRepository,
        category_repo: ICategoryRepository,
    ):
        self._repo = repository
        self.category_repo = category_repo

    async def add_transaction(
        self, transaction: TransactionEntity
    ) -> TransactionEntity:
        await self._repo.add(transaction)
