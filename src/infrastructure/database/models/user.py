# app/infrastructure/models/user.py
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import (
    Column,
    DateTime,
    SQLModel,
    Field,
    Relationship,
    func,
    Enum as SAEnum,
)

from src.domain.value_objects.currency_enum import CurrencyEnum


if TYPE_CHECKING:
    from src.infrastructure.database.models import TransactionModel, CategoryModel


class UserModel(SQLModel, table=True):
    __tablename__: str = "users" # type: ignore


    id: Optional[int] = Field(default=None, primary_key=True)
    tg_id: int = Field(unique=True, index=True)
    username: Optional[str] = Field(default=None, index=True)
    full_name: Optional[str] = Field(default=None)
    monthly_budget: Optional[str] = Field(default=None)
    currency: Optional[CurrencyEnum] = Field(
        sa_column=Column(
            SAEnum(CurrencyEnum, name="currency_enum"),
            nullable=True,
        )
    )
    is_admin: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    password_hash: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=True,
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True,
        )
    )

    category_rel: list["CategoryModel"] = Relationship(back_populates="user_rel")
    transaction_rel: list["TransactionModel"] = Relationship(back_populates="user_rel")
