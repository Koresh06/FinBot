from logging import getLogger

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Back, Next

from src.presentation.bot.users.profile.getters import my_profile_details
from src.presentation.bot.users.profile.states import MyProfile


logger = getLogger(__name__)


router = Router()


my_profile_dialog = Dialog(
    Window(
        Format(
            "🧾 <b>Мой профиль</b>\n\n"
            "👤 <b>Полное имя:</b> {full_name}\n"
            "🔗 <b>Username:</b> @{username}\n"
            "🆔 <b>TG ID:</b> {tg_id}\n"
            "💰 <b>Месячный бюджет:</b> {monthly_budget}\n"
        ),
        state=MyProfile.start,
        getter=my_profile_details,
    )
)


@router.message(Command("profile"))
async def process_command_profile(
    message: Message,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(state=MyProfile.start)
