import pytest
from src.domain.entities.user import UserEntity, CurrencyEnum
from src.infrastructure.repositories.memory.user_repo import UserMemoryRepositoryImpl


@pytest.mark.asyncio
async def test_register_and_get_user():
    repo = UserMemoryRepositoryImpl()

    user = UserEntity(
        id=0,
        tg_id=1234567890,
        username="qwert",
        full_name="QWERT",
        monthly_budget=123.123,
        currency=CurrencyEnum.USD,
    )

    # Тестируем регистрацию
    registered_user = await repo.register(user)

    assert registered_user.id == 1
    assert registered_user.tg_id == user.tg_id
    assert registered_user.username == user.username
    assert registered_user.full_name == user.full_name

    # Тестируем получение по tg_id
    fetched_user = await repo.get_by_tg_id(user.tg_id)

    assert fetched_user is not None
    assert fetched_user.tg_id == user.tg_id
    assert fetched_user.username == user.username
    assert fetched_user.full_name == user.full_name


@pytest.mark.asyncio
async def test_get_by_tg_id_not_found():
    repo = UserMemoryRepositoryImpl()

    # Попытка получить несуществующего пользователя
    user = await repo.get_by_tg_id(999999999)
    assert user is None


@pytest.mark.asyncio
async def test_register_multiple_users():
    repo = UserMemoryRepositoryImpl()

    user1 = UserEntity(
        id=0,
        tg_id=111,
        username="user1",
        full_name="User One",
        monthly_budget=100.0,
        currency=CurrencyEnum.EUR,
    )
    user2 = UserEntity(
        id=0,
        tg_id=222,
        username="user2",
        full_name="User Two",
        monthly_budget=200.0,
        currency=CurrencyEnum.USD,
    )

    registered1 = await repo.register(user1)
    registered2 = await repo.register(user2)

    assert registered1.id == 1
    assert registered2.id == 2

    assert (await repo.get_by_tg_id(111)).username == "user1"
    assert (await repo.get_by_tg_id(222)).username == "user2"
