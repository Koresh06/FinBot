from dataclasses import dataclass, field
from datetime import datetime

from src.domain.value_objects.operetion_type_enum import OperationType


@dataclass
class TransactionEntity:
    user_id: int
    category_id: int
    amount: float
    type: OperationType
    comment: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None
 