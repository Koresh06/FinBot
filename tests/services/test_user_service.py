import pytest
from unittest.mock import AsyncMock

from src.application.services.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFountError,
)
from src.application.services.users.user_service import UserServiceImpl
from src.domain.entities.user import UserEntity
from src.domain.repositories.user_repo_intarface import IUserRepository


@pytest.mark.asyncio
async def test_register_user_success():
    # Мокаем репозиторий

    mock_repo = AsyncMock(spec=IUserRepository)
    mock_repo.get_by_tg_id.return_value = None
    mock_repo.register.return_value = UserEntity(
        id=1, tg_id=123, username="john", full_name="John Doe"
    )

    service = UserServiceImpl(repository=mock_repo)

    user = UserEntity(id=0, tg_id=123, username="john", full_name="John Doe")
    result = await service.register_user(user)

    assert result.id == 1
    mock_repo.register.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_register_user_already_exists():
    # Мокаем существующего пользователя

    mock_repo = AsyncMock(spec=IUserRepository)
    mock_repo.get_by_tg_id.return_value = UserEntity(
        id=1, tg_id=123, username="john", full_name="John Doe"
    )

    service = UserServiceImpl(repository=mock_repo)

    user = UserEntity(id=0, tg_id=123, username="john", full_name="John Doe")

    with pytest.raises(UserAlreadyExistsError):
        await service.register_user(user)


@pytest.mark.asyncio
async def test_get_user_by_tg_id_success():
    mock_repo = AsyncMock(spec=IUserRepository)
    mock_repo.get_by_tg_id.return_value = UserEntity(
        id=1, tg_id=123, username="john", full_name="John Doe"
    )

    service = UserServiceImpl(repository=mock_repo)

    user = await service.get_user_by_tg_id(123)

    assert user.tg_id == 123
    mock_repo.get_by_tg_id.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_get_user_by_tg_id_not_found():
    mock_repo = AsyncMock(spec=IUserRepository)
    mock_repo.get_by_tg_id.return_value = None

    service = UserServiceImpl(repository=mock_repo)

    with pytest.raises(UserNotFountError):
        await service.get_user_by_tg_id(123)


@pytest.mark.asyncio
async def test_set_balance():
    mock_repo = AsyncMock(spec=IUserRepository)
    user = UserEntity(id=1, tg_id=123, username="john", full_name="John Doe")
    mock_repo.get_by_tg_id.return_value = user
    mock_repo.update.return_value = user

    service = UserServiceImpl(repository=mock_repo)

    await service.set_balance(123, 5000.0)

    result = await service.get_user_by_tg_id(123)

    assert result.balance == 5000.0
    mock_repo.update.assert_called_once()
