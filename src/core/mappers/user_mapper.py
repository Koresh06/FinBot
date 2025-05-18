from dataclasses import asdict
from src.domain.entities.user import UserEntity
from src.infrastructure.database.models.user import UserModel


# def db_to_domain(user: UserModel) -> UserEntity:
#     return UserEntity(
#         id=user.id,
#         tg_id=user.tg_id,
#         username=user.username,
#         full_name=user.full_name,
#         is_admin=user.is_admin,
#         is_superuser=user.is_superuser,
#         password_hash=user.password_hash,
#         created_at=user.created_at,
#     )



# def domain_to_db(user: UserEntity) -> UserModel:
#     return UserModel(
#         id=user.id,
#         tg_id=user.tg_id,
#         username=user.username,
#         full_name=user.full_name,
#         is_admin=user.is_admin,
#         is_superuser=user.is_superuser,
#         password_hash=user.password_hash,
#         created_at=user.created_at,
#     )


def db_to_domain(user: UserModel) -> UserEntity:
    return UserEntity(**user.model_dump(exclude={"updated_at"}))

def domain_to_db(user: UserEntity) -> UserModel:
    return UserModel(**asdict(user))
