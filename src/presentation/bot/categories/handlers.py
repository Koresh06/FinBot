from logging import getLogger
from typing import cast
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from src.application.containers.container import Container
from src.domain.entities.category import CategoryEntity
from src.domain.use_case.intarface import UseCaseOneEntity
from src.presentation.bot.transactions.add.states import TransactionDefault


logger = getLogger(__name__)


async def create_category_error_handler(
    message: Message,
    widget: ManagedTextInput[str], 
    dialog_manager: DialogManager,
    error: ValueError, 
) -> None:
    await message.answer("Указана неверное название категории!")


async def save_category_handler(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    container: Container = cast(Container, dialog_manager.middleware_data["container"]) # type: ignore
    use_case: UseCaseOneEntity[CategoryEntity] = container.create_category_uc()

    name: str = dialog_manager.find("cat").get_value() # type: ignore
    await use_case.execute(callback.from_user.id, name.capitalize())

    await callback.answer(text="✅ Категория добавлена!")
    await dialog_manager.start(state=TransactionDefault.start)