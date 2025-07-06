from dataclasses import dataclass, field

from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.transaction_repo_interface import ITransactionRepository


@dataclass
class TransactionMemoryRepositoryImpl(ITransactionRepository):
    items: list[TransactionEntity] = field(default_factory=list)
    counter: int = 1

    def snapshot(self):
        import copy
        return copy.deepcopy(self.items)

    def restore(self, state):
        self.items = state

    async def add(self, transaction: TransactionEntity) -> TransactionEntity:
        new_transaction = TransactionEntity(
            id=self.counter,
            tg_id=transaction.tg_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            type=transaction.type,
            comment=transaction.comment,
        )
        self.counter += 1
        self.items.append(new_transaction)
        return new_transaction

    async def get_by_user(self, tg_id: int) -> list[TransactionEntity]:
        return [t for t in self.items if t.tg_id == tg_id]
