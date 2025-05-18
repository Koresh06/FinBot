from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.entities.enums.transaction_type_enum import TransactionTypeEnum


@dataclass
class TransactionEntity:
    user_id: int
    category_id: int
    amount: float
    type: TransactionTypeEnum
    created_at: datetime
    comment: Optional[str] = None
    id: Optional[int] = None
