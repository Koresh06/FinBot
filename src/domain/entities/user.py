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
    monthly_budget: float = field(default=0.0)
    currency: CurrencyEnum | None = None
    is_admin: bool = False
    is_superuser: bool = False
    password_hash: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None

    def decrease_balance(self, value: float):
        self.monthly_budget -= value

    def increase_balance(self, value: float):
        self.monthly_budget += value