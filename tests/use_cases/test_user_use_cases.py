import pytest
from unittest.mock import AsyncMock

from src.application.use_cases.user.use_cases import GetUserByTgIdUseCase, RegisterUserUseCase
from src.domain.entities.user import UserEntity
from src.application.services.categories.interface import ICategoryService
from src.application.services.users.interface import IUserService


@pytest.mark.asyncio
async def test_register_user_use_case_success():
    """Проверяем успешную регистрацию пользователя и создание дефолтных категорий"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    test_user = UserEntity(id=1, tg_id=123, full_name="Test", username="testuser")
    mock_user_service.register_user.return_value = test_user

    use_case = RegisterUserUseCase(
        user_service=mock_user_service,
        category_service=mock_category_service,
    )

    result = await use_case.execute(test_user)

    assert result.id == 1
    mock_user_service.register_user.assert_called_once_with(test_user)
    mock_category_service.create_default_categories.assert_called_once_with(test_user.id)


@pytest.mark.asyncio
async def test_register_user_use_case_raises_when_id_is_none():
    """Проверяем, что если после регистрации user.id = None — выбрасывается ошибка"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    test_user = UserEntity(id=None, tg_id=123, full_name="Test", username="testuser")
    mock_user_service.register_user.return_value = test_user

    use_case = RegisterUserUseCase(
        user_service=mock_user_service,
        category_service=mock_category_service,
    )

    with pytest.raises(ValueError, match="User ID is None after registration"):
        await use_case.execute(test_user)


@pytest.mark.asyncio
async def test_get_user_by_tg_id_use_case_success():
    """Проверяем, что юзер успешно возвращается по tg_id"""
    mock_user_service = AsyncMock(spec=IUserService)
    user = UserEntity(id=1, tg_id=123, full_name="Test", username="testuser")
    mock_user_service.get_user_by_tg_id.return_value = user

    use_case = GetUserByTgIdUseCase(user_service=mock_user_service)

    result = await use_case.execute(123)

    assert result.tg_id == 123
    mock_user_service.get_user_by_tg_id.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_get_user_by_tg_id_user_not_found():
    """Проверяем, что None возвращается, если пользователь не найден"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_user_service.get_user_by_tg_id.return_value = None

    use_case = GetUserByTgIdUseCase(user_service=mock_user_service)

    result = await use_case.execute(999)

    assert result is None
    mock_user_service.get_user_by_tg_id.assert_called_once_with(999)
