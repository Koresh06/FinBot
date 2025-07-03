from typing import List, Optional, Sequence
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.category_repo import ICategoryRepository
from src.domain.entities.category import CategoryEntity
from src.infrastructure.database.models.category import CategoryModel
from src.utils.mappers.category_mapper import db_to_domain


class CategorySQLiteRepositoryImpl(ICategoryRepository):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory


    async def get_user_categories(self, user_id: int) -> List[CategoryEntity]:
        async with self.session_factory() as session:
            stmt = await session.execute(select(CategoryModel).where(CategoryModel.user_id == user_id))
            categories_result: Sequence[CategoryModel] = stmt.scalars().all()

            return [db_to_domain(cat) for cat in categories_result]

            
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
            stmt = await session.execute(select(CategoryModel).where(
                CategoryModel.user_id == user_id,
                CategoryModel.name == name
            ))
            category_result: Optional[CategoryModel] = stmt.scalar_one_or_none()

            if category_result:
                return db_to_domain(category_result)
            return None