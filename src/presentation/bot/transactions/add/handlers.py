from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button


async def save_type_transaction(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    selected_type = button.widget_id  # 'income' или 'expense'
    dialog_manager.dialog_data["transaction_type"] = selected_type # type: ignore

    await dialog_manager.next()


async def save_category(
    callback: CallbackQuery,
    widget: Select[str],
    dialog_manager: DialogManager,
    item_id: str
) -> None:
    dialog_manager.dialog_data["cat_id"] = int(item_id) # type: ignore
    
    await callback.answer(item_id)
    # await dialog_manager.next()

