from logging import getLogger
from typing import cast
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from src.application.containers.container import Container
from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType
from src.application.use_cases.intarface import UseCaseOneEntity
from src.presentation.bot.logic.transactions.add_default.states import TransactionDefault


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
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseOneEntity[CategoryEntity] = container.create_category_uc()

    name: str = dialog_manager.find("cat").get_value() 
    type: OperationType = OperationType(dialog_manager.start_data["type"]) # type: ignore

    await use_case.execute(tg_id=callback.from_user.id, type=type, name=name.capitalize())

    await callback.answer(text="✅ Категория добавлена!")
    await dialog_manager.start(state=TransactionDefault.start)