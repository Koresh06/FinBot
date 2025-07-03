from enum import Enum


class OperationType(str, Enum):
    income = "income"
    expense = "expense"
