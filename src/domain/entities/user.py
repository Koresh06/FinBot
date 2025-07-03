# app/domain/entities/user.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from src.domain.value_objects.currency_enum import CurrencyEnum


@dataclass
class UserEntity:
    tg_id: int
    username: Optional[str]
    full_name: Optional[str]
    monthly_budget: Optional[float] = None
    currency: Optional[CurrencyEnum] = None
    is_admin: bool = False
    is_superuser: bool = False
    password_hash: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None