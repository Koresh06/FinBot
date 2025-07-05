# app/domain/entities/user.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from src.domain.value_objects.currency_enum import CurrencyEnum


@dataclass
class UserEntity:
    tg_id: int
    username: str | None
    full_name: str | None
    balance: float = field(default=0.0)
    currency: CurrencyEnum = field(default=CurrencyEnum.RUB)
    is_admin: bool = False
    is_superuser: bool = False
    password_hash: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None

    def decrease_balance(self, value: float):
        self.balance -= value

    def increase_balance(self, value: float):
        self.balance += value
