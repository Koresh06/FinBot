from dataclasses import dataclass, field
from datetime import datetime

from src.domain.value_objects.currency_enum import CurrencyEnum


@dataclass
class UserDTO:
    tg_id: int
    username: str | None
    full_name: str | None
    monthly_budget: float | None = None
    currency: CurrencyEnum | None = None
    is_admin: bool = False
    is_superuser: bool = False
    password_hash: str | None = None
    created_at: datetime = field(default_factory=datetime.now)