from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.category_repo import ICategoryRepository
from src.domain.repositories.transaction_use_case import ITransactionRepository
from src.application.services.transactions.interface import ITransactionService


class TransactionServiceImpl(ITransactionService):

    def __init__(
        self,
        transaction_repo: ITransactionRepository,
    ):
        self.transaction_repo = transaction_repo

    async def add_transaction(
        self, transaction: TransactionEntity
    ) -> TransactionEntity:
        return await self.transaction_repo.add(transaction)

