from dataclasses import dataclass, field

from src.domain.entities.transaction import TransactionEntity
from src.domain.value_objects.operetion_type_enum import OperationType


@dataclass
class MonthlyBalance:
    tg_id: int
    year: int
    month: int
    income: float = field(default=0.0)
    expense: float = field(default=0.0)
    balance: float = field(default=0.0)
    id: int | None = None

    def apply_transaction(self, transaction: TransactionEntity):
        if transaction.type == OperationType.expense:
            self.expense += transaction.amount
            self.balance -= transaction.amount
        elif transaction.type == OperationType.income:
            self.income += transaction.amount
            self.balance += transaction.amount
        else:
            raise ValueError(f"Unknown transaction type: {transaction.type}")