from aiogram import Router
from aiogram_dialog import Dialog

from src.presentation.bot.users.registration.dialogs import router as user_router
from src.presentation.bot.transactions.add.dialogs import router as transaction_router

from src.presentation.bot.transactions.add.dialogs import (
    add_transaction_dialog,
    transaction_default_dialiog,
)
from src.presentation.bot.categories.dialogs import create_category_dialog


def get_all_dialogs() -> list[Dialog]:
    return [
        add_transaction_dialog,
        transaction_default_dialiog,
        create_category_dialog,
    ]


def get_routers() -> list[Router]:
    return [
        user_router,
        transaction_router,
    ]
