from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.transaction_repo_interface import ITransactionRepository


class TransactionMemoryRepositoryImpl(ITransactionRepository):
    def __init__(self):
        self.transactions: list[TransactionEntity] = []
        self.counter = 1

    def snapshot(self):
        import copy
        return copy.deepcopy(self.transactions)

    def restore(self, state):
        self.transactions = state

    async def add(self, transaction: TransactionEntity) -> TransactionEntity:
        new_transaction = TransactionEntity(
            id=self.counter,
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            type=transaction.type,
            comment=transaction.comment,
        )
        self.counter += 1
        self.transactions.append(new_transaction)
        return new_transaction

    async def get_by_user(self, user_id: int) -> list[TransactionEntity]:
        return [t for t in self.transactions if t.user_id == user_id]
