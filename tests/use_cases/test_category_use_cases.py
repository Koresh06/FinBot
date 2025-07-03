import pytest
from unittest.mock import AsyncMock

from src.application.services.categories.exceptions import CategoryAlreadyExistsError
from src.application.use_cases.category.use_cases import CreateCategoryUserUseCase, GetCategoriesOfUserUseCase
from src.domain.entities.user import UserEntity
from src.domain.entities.category import CategoryEntity
from src.application.services.categories.interface import ICategoryService
from src.application.services.users.interface import IUserService



@pytest.mark.asyncio
async def test_get_categories_of_user_success():
    """ Проверяем успешное получение категорий пользователя по tg_id"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    user = UserEntity(id=1, tg_id=123, full_name="Test", username="testuser")
    categories = [
        CategoryEntity(id=1, name="Еда", user_id=1),
        CategoryEntity(id=2, name="Транспорт", user_id=1),
    ]

    mock_user_service.get_user_by_tg_id.return_value = user
    mock_category_service.get_user_categories.return_value = categories

    use_case = GetCategoriesOfUserUseCase(
        category_service=mock_category_service,
        user_service=mock_user_service,
    )

    result = await use_case.execute(123)

    assert len(result) == 2
    mock_user_service.get_user_by_tg_id.assert_called_once_with(123)
    mock_category_service.get_user_categories.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_categories_of_user_user_not_found():
    """ Проверяем, что выбрасывается ошибка, если пользователь не найден"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    mock_user_service.get_user_by_tg_id.return_value = None

    use_case = GetCategoriesOfUserUseCase(
        category_service=mock_category_service,
        user_service=mock_user_service,
    )

    with pytest.raises(ValueError, match="Пользователь с tg_id=123 не найден"):
        await use_case.execute(123)


@pytest.mark.asyncio
async def test_create_category_user_use_case_success():
    """ Проверяем успешное создание категории для пользователя по tg_id"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    user = UserEntity(id=1, tg_id=123, full_name="Test", username="testuser")
    mock_user_service.get_user_by_tg_id.return_value = user

    use_case = CreateCategoryUserUseCase(
        category_service=mock_category_service,
        user_service=mock_user_service,
    )

    await use_case.execute(tg_id=123, name="Путешествия")

    mock_user_service.get_user_by_tg_id.assert_called_once_with(123)
    mock_category_service.create_category.assert_called_once()
    created_category = mock_category_service.create_category.call_args[0][0]
    assert created_category.name == "Путешествия"
    assert created_category.user_id == 1


@pytest.mark.asyncio
async def test_create_category_user_use_case_already_exists():
    """ Проверяем обработку ошибки при попытке создать существующую категорию"""
    mock_user_service = AsyncMock(spec=IUserService)
    mock_category_service = AsyncMock(spec=ICategoryService)

    user = UserEntity(id=1, tg_id=123, full_name="Test", username="testuser")
    mock_user_service.get_user_by_tg_id.return_value = user
    mock_category_service.create_category.side_effect = CategoryAlreadyExistsError("уже существует")

    use_case = CreateCategoryUserUseCase(
        category_service=mock_category_service,
        user_service=mock_user_service,
    )

    with pytest.raises(CategoryAlreadyExistsError, match="уже существует"):
        await use_case.execute(tg_id=123, name="Еда")
