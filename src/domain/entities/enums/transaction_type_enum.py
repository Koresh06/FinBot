from enum import Enum


class TransactionTypeEnum(str, Enum):
    income = "income"
    expense = "expense"
