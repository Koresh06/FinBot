from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.value_objects.transaction_type_enum import TransactionTypeEnum


@dataclass
class TransactionEntity:
    user_id: int
    category_id: int
    amount: float
    type: TransactionTypeEnum
    created_at: datetime = field(default_factory=datetime.now)
    comment: Optional[str] = None
    id: Optional[int] = None
