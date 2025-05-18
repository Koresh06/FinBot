# app/infrastructure/models/category.py
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from src.infrastructure.database.models import TransactionModel, UserModel


class CategoryModel(SQLModel, table=True):
    __tablename__ = "categories" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str = Field(index=True)

    user_rel: list["UserModel"] = Relationship(back_populates="category_rel")
    transaction_rel: list["TransactionModel"] = Relationship(back_populates="category_rel")
