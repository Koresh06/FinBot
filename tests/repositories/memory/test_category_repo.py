import pytest
from src.domain.entities.category import CategoryEntity
from src.infrastructure.repositories.memory.category_repo import CategoryMemoryRepositoryImpl


@pytest.mark.asyncio
async def test_create_category():
    # Проверяем создание одной категории и сохранение её в памяти
    repo = CategoryMemoryRepositoryImpl()

    category = CategoryEntity(id=0, name="Food", user_id=1)
    created_category = await repo.create(category)

    assert created_category.id == 1
    assert created_category.name == "Food"
    assert created_category.user_id == 1

    user_categories = await repo.get_user_categories(1)
    assert len(user_categories) == 1
    assert user_categories[0].name == "Food"


@pytest.mark.asyncio
async def test_get_user_categories_empty():
    # Проверяем, что у нового пользователя категорий нет
    repo = CategoryMemoryRepositoryImpl()
    categories = await repo.get_user_categories(99)
    assert categories == []


@pytest.mark.asyncio
async def test_create_multiple_categories_for_user():
    # Проверяем добавление нескольких категорий одному пользователю
    repo = CategoryMemoryRepositoryImpl()

    await repo.create(CategoryEntity(id=0, name="Food", user_id=1))
    await repo.create(CategoryEntity(id=0, name="Transport", user_id=1))

    categories = await repo.get_user_categories(1)

    assert len(categories) == 2
    assert {cat.name for cat in categories} == {"Food", "Transport"}


@pytest.mark.asyncio
async def test_get_by_user_and_name_found():
    # Проверяем поиск категории по имени и user_id — успешный случай
    repo = CategoryMemoryRepositoryImpl()

    await repo.create(CategoryEntity(id=0, name="Groceries", user_id=2))
    found = await repo.get_by_user_and_name(user_id=2, name="Groceries")

    assert found is not None
    assert found.name == "Groceries"
    assert found.user_id == 2


@pytest.mark.asyncio
async def test_get_by_user_and_name_not_found():
    # Проверяем случай, когда категория с таким именем не найдена
    repo = CategoryMemoryRepositoryImpl()

    await repo.create(CategoryEntity(id=0, name="Rent", user_id=3))
    result = await repo.get_by_user_and_name(user_id=3, name="Other")

    assert result is None
