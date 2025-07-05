from aiogram import Router
from aiogram_dialog import Dialog

from src.presentation.bot.logic.users.registration.dialogs import router as user_router
from src.presentation.bot.logic.transactions.add_default.dialogs import router as transaction_router
from src.presentation.bot.logic.users.profile.dialogs import router as profile_user_router

from src.presentation.bot.logic.transactions.add_default.dialogs import (
    add_transaction_dialog,
    transaction_default_dialiog,
)
from src.presentation.bot.logic.transactions.add_ai.dialogs import add_transaction_ai_dialog
from src.presentation.bot.logic.categories.dialogs import create_category_dialog
from src.presentation.bot.logic.users.profile.dialogs import my_profile_dialog


def get_all_dialogs() -> list[Dialog]:
    return [
        add_transaction_dialog,
        transaction_default_dialiog,
        create_category_dialog,
        my_profile_dialog,
        add_transaction_ai_dialog,
    ]


def get_routers() -> list[Router]:
    return [
        user_router,
        transaction_router,
        profile_user_router,
    ]
