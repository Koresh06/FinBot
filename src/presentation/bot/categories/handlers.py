from logging import getLogger
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput

from src.application.containers.container import Container
from src.domain.use_case.intarface import UseCaseOneEntity
from src.presentation.bot.transactions.add.states import TransactionDefault


logger = getLogger(__name__)


async def create_category_error_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    await message.answer("Указана неверное название категории!")


async def save_category_handler(
    callback: CallbackQuery,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
) -> None:
    container: Container = dialog_manager.middleware_data["container"]
    use_case: UseCaseOneEntity = container.create_category_uc()

    name: TextInput = dialog_manager.find("cat").get_value()
    await use_case.execute(callback.from_user.id, name.capitalize())

    logger.info(f"Пользователь: {callback.from_user.id} создал категорию - {name.capitalize()})")
    await callback.answer(text="✅ Категория добавлена!")
    await dialog_manager.start(state=TransactionDefault.start)