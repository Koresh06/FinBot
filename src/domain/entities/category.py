# app/domain/entities/category.py
from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects.operetion_type_enum import OperationType


DEFAULT_CATEGORIES = {
    "expense": [
        "Продукты",
        "Транспорт",
        "Жильё",
        "Развлечения",
        "Подарки",
    ],
    "income": [
        "Зарплата",
        "Подарки",
    ],
}



@dataclass
class CategoryEntity:
    user_id: int
    name: str
    type: OperationType
    id: int | None = None
