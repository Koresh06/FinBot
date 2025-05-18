

from src.domain.entities.transaction import TransactionEntity
from src.domain.repositories.transaction_use_case import ITransactionRepository


class TransactionMemoryRepositoryImpl(ITransactionRepository):
    def __init__(self):
        self.transactions: dict[int, TransactionEntity] = {} 
        self.counter = 1