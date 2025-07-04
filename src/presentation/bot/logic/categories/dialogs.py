from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Start, Button, Next
from aiogram_dialog.widgets.input import TextInput

from src.presentation.bot.categories.gatters import cate_name_getter
from src.presentation.bot.categories.handlers import (
    create_category_error_handler,
    save_category_handler,
)
from src.presentation.bot.categories.states import CreateCategory
from src.presentation.bot.transactions.add.states import TransactionDefault


router = Router()


create_category_dialog = Dialog(
    Window(
        Const("Укажите название категории"),
        TextInput(
            id="cat",
            type_factory=str,
            on_success=Next(),
            on_error=create_category_error_handler,
        ),
        Start(
            Const("⬅️ Назад"),
            id="all_cats",
            state=TransactionDefault.cat,
        ),
        state=CreateCategory.name,
    ),
    Window(
        Format("Подтвердите название категории: {cat_name}"),
        Button(
            Const("✅ Подтвердить"),
            id="confirm",
            on_click=save_category_handler,
        ),
        state=CreateCategory.confirm,
        getter=cate_name_getter,
    ),
)
