import pytest
from unittest.mock import AsyncMock

from src.application.services.categories.exceptions import CategoryAlreadyExistsError
from src.application.services.categories.category_service import CategoryServiceImpl
from src.domain.entities.category import CategoryEntity, DEFAULT_CATEGORIES
from src.domain.repositories.category_repo_interface import ICategoryRepository


@pytest.mark.asyncio
async def test_get_user_categories():
    # Проверяем получение всех категорий пользователя

    mock_repo = AsyncMock(spec=ICategoryRepository)
    mock_repo.get_user_categories.return_value = [
        CategoryEntity(id=1, name="Еда", user_id=123)
    ]

    service = CategoryServiceImpl(category_repo=mock_repo)

    result = await service.get_user_categories(123)

    assert len(result) == 1
    assert result[0].name == "Еда"
    mock_repo.get_user_categories.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_create_category_success():
    # Проверяем успешное создание новой категории

    mock_repo = AsyncMock(spec=ICategoryRepository)
    mock_repo.get_by_user_and_name.return_value = None
    mock_repo.create.return_value = CategoryEntity(id=1, name="Еда", user_id=123)

    service = CategoryServiceImpl(category_repo=mock_repo)

    category = CategoryEntity(name="Еда", user_id=123)
    result = await service.create_category(category)

    assert result.name == "Еда"
    mock_repo.create.assert_called_once_with(category)


@pytest.mark.asyncio
async def test_create_category_already_exists():
    # Проверяем, что ошибка выбрасывается при попытке создать уже существующую категорию

    mock_repo = AsyncMock(spec=ICategoryRepository)
    mock_repo.get_by_user_and_name.return_value = CategoryEntity(
        id=1, name="Еда", user_id=123
    )

    service = CategoryServiceImpl(category_repo=mock_repo)

    category = CategoryEntity(name="Еда", user_id=123)

    with pytest.raises(CategoryAlreadyExistsError):
        await service.create_category(category)


@pytest.mark.asyncio
async def test_create_default_categories():
    # Проверяем создание всех дефолтных категорий

    mock_repo = AsyncMock(spec=ICategoryRepository)
    mock_repo.get_by_user_and_name.return_value = None
    mock_repo.create.side_effect = lambda cat: CategoryEntity(
        id=1,
        name=cat.name,
        user_id=cat.user_id,
    )

    service = CategoryServiceImpl(category_repo=mock_repo)

    await service.create_default_categories(user_id=123)

    assert mock_repo.create.call_count == len(DEFAULT_CATEGORIES)
    for name in DEFAULT_CATEGORIES:
        mock_repo.get_by_user_and_name.assert_any_call(user_id=123, name=name)

