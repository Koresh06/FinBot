from sqlalchemy import select

from src.domain.repositories.user_repo_intarface import IUserRepository
from src.domain.entities.user import UserEntity
from src.infrastructure.database.models.user import UserModel
from src.core.mappers.user_mapper import db_to_domain, domain_to_db



class UserSQLiteRepositoryImpl(IUserRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def register(self, user: UserEntity) -> UserEntity:
        async with self.session_factory() as session:
            db_user = domain_to_db(user)
            new_user = UserModel(
                tg_id=db_user.tg_id,
                username=db_user.username,
                full_name=db_user.full_name,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return db_to_domain(new_user)

    async def get_by_tg_id(self, tg_id: int) -> UserEntity | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.tg_id == tg_id)
            )
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return db_to_domain(user)
        

    async def update(self, user: UserEntity) -> UserEntity:
        async with self.session_factory() as session:
            db_user = await session.get(UserModel, user.id)
            if not db_user:
                raise ValueError(f"User with id={user.id} not found")

            user_data = domain_to_db(user)

            for key, value in user_data.items():
                if key != "id" and value is not None:
                    setattr(db_user, key, value)

            await session.commit()
            await session.refresh(db_user)
            return db_to_domain(db_user)

