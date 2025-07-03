# app/infrastructure/models/category.py
from typing import TYPE_CHECKING, Optional
from sqlmodel import Column, SQLModel, Field, Relationship, Enum as SAEnum

from src.domain.value_objects.operetion_type_enum import OperationType


if TYPE_CHECKING:
    from src.infrastructure.database.models import TransactionModel, UserModel


class CategoryModel(SQLModel, table=True):
    __tablename__ = "categories" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str = Field(index=True)
    type: OperationType = Field(
        sa_column=Column(
            SAEnum(OperationType, name="operation_type_enum"),
            nullable=False,
        )
    )

    user_rel: list["UserModel"] = Relationship(back_populates="category_rel")
    transaction_rel: list["TransactionModel"] = Relationship(back_populates="category_rel")
