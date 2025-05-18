from typing import Optional
from sqlmodel import select
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.category_repo import ICategoryRepository
from src.domain.entities.category import CategoryEntity
from src.infrastructure.database.models.category import CategoryModel
from src.core.mappers.category_mapper import db_to_domain


class CategorySQLiteRepositoryImpl(ICategoryRepository):

    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def get_user_categories(self, user_id: int) -> list[CategoryEntity]:
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(CategoryModel.user_id == user_id)
            result: Result = await session.execute(stmt)
            categories = result.scalars()
            return [db_to_domain(cat) for cat in categories]

            
    async def create(self, category: CategoryEntity) -> CategoryEntity:
        async with self.session_factory() as session:
            new_category = CategoryModel(
                name=category.name,
                user_id=category.user_id,
            )
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return db_to_domain(new_category)
        

    async def get_by_user_and_name(self, user_id: int, name: str) -> Optional[CategoryEntity]:
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(
                CategoryModel.user_id == user_id,
                CategoryModel.name == name
            )
            result: Result = await session.execute(stmt)
            category = result.scalar_one_or_none()
            if category:
                return db_to_domain(category)
            return None