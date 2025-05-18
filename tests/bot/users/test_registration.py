import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User
from aiogram_dialog import DialogManager

from src.application.services.users.exceptions import UserAlreadyExistsError
from src.presentation.bot.users.registration.dialogs import command_start_process


@pytest.mark.asyncio
async def test_command_start_process_success():
    message = AsyncMock(spec=Message)
    
    # Создаем мок объекта from_user с нужными атрибутами
    from_user_mock = MagicMock(spec=User)
    from_user_mock.id = 123
    from_user_mock.username = "testuser"
    from_user_mock.full_name = "Test User"
    message.from_user = from_user_mock

    message.answer = AsyncMock()

    dialog_manager = MagicMock(spec=DialogManager)
    use_case_mock = AsyncMock()
    container_mock = MagicMock()
    container_mock.register_user_uc.return_value = use_case_mock
    dialog_manager.middleware_data = {"container": container_mock}

    await command_start_process(message, dialog_manager)

    use_case_mock.execute.assert_awaited_once()
    message.answer.assert_awaited_with(text="Приветствую Вас <b>Test User!</b>")


@pytest.mark.asyncio
async def test_command_start_process_user_already_exists():
    message = AsyncMock(spec=Message)
    from_user_mock = MagicMock(spec=User)
    from_user_mock.id = 123
    from_user_mock.username = "testuser"
    from_user_mock.full_name = "Test User"
    message.from_user = from_user_mock

    message.answer = AsyncMock()

    dialog_manager = MagicMock(spec=DialogManager)
    use_case_mock = AsyncMock()
    use_case_mock.execute.side_effect = UserAlreadyExistsError("Пользователь уже зарегистрирован")
    container_mock = MagicMock()
    container_mock.register_user_uc.return_value = use_case_mock
    dialog_manager.middleware_data = {"container": container_mock}

    await command_start_process(message, dialog_manager)

    message.answer.assert_awaited_with(text="Вы уже зарегистрированы")


@pytest.mark.asyncio
async def test_command_start_process_generic_exception():
    message = AsyncMock(spec=Message)
    from_user_mock = MagicMock(spec=User)
    from_user_mock.id = 123
    from_user_mock.username = "testuser"
    from_user_mock.full_name = "Test User"
    message.from_user = from_user_mock

    message.answer = AsyncMock()

    dialog_manager = MagicMock(spec=DialogManager)
    use_case_mock = AsyncMock()
    use_case_mock.execute.side_effect = Exception("Ошибка!")
    container_mock = MagicMock()
    container_mock.register_user_uc.return_value = use_case_mock
    dialog_manager.middleware_data = {"container": container_mock}

    await command_start_process(message, dialog_manager)

    message.answer.assert_awaited_with("Произошла ошибка. Попробуйте позже.")
