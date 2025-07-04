from logging import getLogger
from typing import cast
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import ManagedTextInput

from src.application.containers.container import Container
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity
from src.domain.entities.transaction import TransactionEntity
from src.presentation.bot.categories.states import CreateCategory


logger = getLogger(__name__)


async def save_type_transaction(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    selected_type = button.widget_id  # 'income' или 'expense'
    dialog_manager.dialog_data["transaction_type"] = selected_type
    await dialog_manager.next()



async def on_add_category_click(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    type: str = dialog_manager.dialog_data["transaction_type"]

    await dialog_manager.start(state=CreateCategory.name, data={"type": type})


async def save_category(
    callback: CallbackQuery,
    widget: Select[str],
    dialog_manager: DialogManager,
    item_id: str
) -> None:
    dialog_manager.dialog_data["cat_id"] = int(item_id)
    await dialog_manager.next()


async def total_sum_error_handler(
    message: Message,
    widget: ManagedTextInput[str], 
    dialog_manager: DialogManager,
    value: ValueError,
) -> None:
    await message.answer("Неверно указана сумма операции. Повторите!!!")


async def confirm_transaction_handler(
    callback: CallbackQuery,
    widget: Button, 
    dialog_manager: DialogManager,
):
    type: str = dialog_manager.dialog_data["transaction_type"]
    cat: int = dialog_manager.dialog_data["cat_id"]
    total_sum: str = dialog_manager.find("total_sum").get_value() 
    comment: str = dialog_manager.find("comment").get_value()

    data = {
        "type": type,
        "category": cat,
        "total_sum": total_sum,
        "comment": comment,
    }

    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseOneEntity[TransactionEntity] = container.add_transac_uv()

    await use_case.execute(tg_id=callback.from_user.id, data=data)
    
    await callback.message.answer("Транзакция успешно добавлена")
    logger.info(f"Пользователь: {callback.from_user.id} добавиль транзакицю: тип - {type}, категория - {cat}, сумма - {total_sum}")
