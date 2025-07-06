from dataclasses import dataclass, field


@dataclass
class MonthlyBalance:
    tg_id: int
    year: int
    month: int
    income: float = field(default=0.0)
    expense: float = field(default=0.0)
    balance: float = field(default=0.0)
    id: int | None = None

    def fucn_income(self, value: float):
        self.income += value
        self.balance -= value

    def func_expense(self, value: float):
        self.expense += value
        self.balance += value
