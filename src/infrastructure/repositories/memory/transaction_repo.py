from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.transaction_use_case import ITransactionRepository


class TransactionMemoryRepositoryImpl(ITransactionRepository):
    def __init__(self):
        self.transactions: dict[int, TransactionEntity] = {} 
        self.counter = 1


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

        if transaction.user_id not in self.transactions:
            self.transactions[transaction.user_id] = []

        self.transactions[transaction.user_id].append(new_transaction)
        return new_transaction