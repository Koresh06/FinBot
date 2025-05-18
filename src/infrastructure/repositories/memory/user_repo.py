from src.domain.repositories.user_repo_intarface import IUserRepository
from src.domain.entities.user import UserEntity



class UserMemoryRepositoryImpl(IUserRepository):
    def __init__(self):
        self.users: dict[int, UserEntity] = {} 
        self.counter = 1

    async def register(self, user: UserEntity) -> UserEntity:
        new_user = UserEntity(
            id=self.counter,
            tg_id=user.tg_id,
            username=user.username,
            full_name=user.full_name,
        )
        self.users[user.tg_id] = new_user
        self.counter += 1
        return new_user

    async def get_by_tg_id(self, tg_id: int) -> UserEntity | None:
        return self.users.get(tg_id)
