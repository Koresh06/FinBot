# app/domain/entities/category.py
from dataclasses import dataclass
from typing import Optional


DEFAULT_CATEGORIES = [
    "Продукты",
    "Транспорт",
    "Жильё",
    "Развлечения",
    "Зарплата",
    "Подарки",
]


@dataclass
class CategoryEntity:
    user_id: int
    name: str
    id: Optional[int] = None
