from dataclasses import dataclass, field

from src.domain.repositories.user_repo_intarface import IUserRepository
from src.domain.entities.user import UserEntity


@dataclass
class UserMemoryRepositoryImpl(IUserRepository):
    users: list[UserEntity] = field(default_factory=list)
    counter: int = 1

    def snapshot(self):
        import copy
        return copy.deepcopy(self.users)

    def restore(self, state):
        self.users = state

    async def register(self, user: UserEntity) -> UserEntity:
        new_user = UserEntity(
            id=self.counter,
            tg_id=user.tg_id,
            username=user.username,
            full_name=user.full_name,
        )
        self.counter += 1
        self.users.append(new_user)
        return new_user

    async def get_by_tg_id(self, tg_id: int) -> UserEntity | None:
        for user in self.users:
            if user.tg_id == tg_id:
                return user
        return None
    
    async def update(self, user_update: UserEntity) -> None:
        for index, user in enumerate(self.users):
            if user.id == user_update.id:
                self.users[index] = user_update
                return
        raise ValueError(f"User with id={user_update.id} not found")