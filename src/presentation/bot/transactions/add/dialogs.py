from aiogram_dialog import DialogManager

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Start, Button, Row, Group, Select, Back

from src.presentation.bot.categories.states import CreateCategory
from src.presentation.bot.transactions.add.getters import getter_categories
from src.presentation.bot.transactions.add.handlers import (
    save_category,
    save_type_transaction,
)
from src.presentation.bot.transactions.add.states import (
    AddTransaction,
    TransactionDefault,
    TransactionFromTextAI,
)


router = Router()


add_transaction_dialog = Dialog(
    Window(
        Const("💼 <b>Выберите способ добавления транзакции:</b>"),
        Start(
            Const("⚙️ Дефолтный способ"),
            id="default",
            state=TransactionDefault.start,
        ),
        Start(
            Const("🤖 AI способ"),
            id="ai",
            state=TransactionFromTextAI.start,
        ),
        state=AddTransaction.start,
    )
)


transaction_default_dialiog = Dialog(
    Window(
        Const("💰 <b>Укажите тип транзакции:</b>"),
        Row(
            Button(Const("📈 Доход"), id="income", on_click=save_type_transaction),
            Button(Const("📉 Расход"), id="expense", on_click=save_type_transaction),
        ),
        state=TransactionDefault.start,
    ),
    Window(
        Format("📂 <b>Выберите категорию.</b>\nТип транзакции: <b>{type_tr}</b>"),
        Group(
            Select(
                Format("📌 {item.name}"),
                id="cat",
                items="categories",
                item_id_getter=lambda c: str(c.id),
                on_click=save_category,
            ),
            width=3,
        ),
        Start(
            Const("➕ Добавить категорию"),
            id="create_cat",
            state=CreateCategory.name,
        ),
        Back(Const("⬅️ Назад")),
        state=TransactionDefault.cat,
        getter=getter_categories,
    ),
)


@router.message(Command("add"))
async def add_transaction(
    message: Message,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(state=AddTransaction.start) # type: ignore
