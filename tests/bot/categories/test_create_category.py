import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.input import ManagedTextInput

from src.presentation.bot.categories.gatters import cate_name_getter
from src.presentation.bot.categories.handlers import create_category_error_handler, save_category_handler
from src.presentation.bot.transactions.add.states import TransactionDefault


@pytest.mark.asyncio
async def test_cate_name_getter():
    dialog_manager = MagicMock()
    dialog_manager.start = AsyncMock()

    text_input_mock = MagicMock(spec=ManagedTextInput)
    text_input_mock.get_value.return_value = "testcategory"
    dialog_manager.find.return_value = text_input_mock

    result = await cate_name_getter(dialog_manager)
    assert result == {"cat_name": "Testcategory"}
    dialog_manager.find.assert_called_with("cat")


@pytest.mark.asyncio
async def test_create_category_error_handler():
    message = AsyncMock(spec=Message)
    # Заменяем message.answer на AsyncMock, чтобы поддерживал await
    message.answer = AsyncMock()

    widget = MagicMock(spec=ManagedTextInput)
    dialog_manager = MagicMock()
    dialog_manager.start = AsyncMock()

    text = "some error"

    await create_category_error_handler(message, widget, dialog_manager, text)
    message.answer.assert_awaited_once_with("Указана неверное название категории!")


@pytest.mark.asyncio
async def test_save_category_handler():
    callback = AsyncMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123

    # Заменяем callback.answer на AsyncMock
    callback.answer = AsyncMock()

    widget = MagicMock(spec=ManagedTextInput)
    dialog_manager = MagicMock()
    dialog_manager.start = AsyncMock()

    dialog_manager.middleware_data = {
        "container": MagicMock(create_category_uc=MagicMock())
    }
    use_case_mock = dialog_manager.middleware_data["container"].create_category_uc.return_value
    use_case_mock.execute = AsyncMock()

    dialog_manager.find.return_value.get_value.return_value = "testcategory"

    await save_category_handler(callback, widget, dialog_manager)

    use_case_mock.execute.assert_awaited_once_with(123, "Testcategory")
    callback.answer.assert_awaited_once_with(text="✅ Категория добавлена!")
    dialog_manager.start.assert_awaited_once_with(state=TransactionDefault.start)
