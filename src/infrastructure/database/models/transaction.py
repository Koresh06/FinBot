# app/infrastructure/models/transaction.py
from sqlmodel import Column, SQLModel, Field, Relationship, Enum as SAEnum
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from src.domain.entities.enums.transaction_type_enum import TransactionTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel, CategoryModel


class TransactionModel(SQLModel, table=True):
    __tablename__ = "transactions" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    category_id: int = Field(foreign_key="categories.id")
    amount: float
    type: TransactionTypeEnum = Field(
        sa_column=Column(
            SAEnum(TransactionTypeEnum, name="transaction_type_enum"),
            nullable=False,
        )
    )
    comment: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    user_rel: Optional["UserModel"] = Relationship(back_populates="transaction_rel")
    category_rel: Optional["CategoryModel"] = Relationship(
        back_populates="transaction_rel"
    )
