from logging import getLogger
from typing import cast

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager

from src.application.services.users.exceptions import UserAlreadyExistsError
from src.application.use_cases.intarface import UseCaseOneEntity
from src.domain.entities.user import UserEntity
from src.application.containers.container import Container


logger = getLogger(__name__)


router = Router()


@router.message(CommandStart())
async def command_start_process(
    message: Message,
    dialog_manager: DialogManager,
):
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    try:
        use_case: UseCaseOneEntity[UserEntity] = container.register_user_uc()

        await use_case.execute(
            UserEntity(
                tg_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
            )
        )

        logger.info(f"✅ Зарегистрирован новый пользователь: {message.from_user.full_name} ({message.from_user.id})")
        await message.answer(text=f"Приветствую Вас <b>{message.from_user.full_name}!</b>")

    except UserAlreadyExistsError:
        logger.info(f"⚠️ Пользователь уже зарегистрирован: {message.from_user.full_name} ({message.from_user.id})")
        await message.answer(text="Вы уже зарегистрированы")

    except Exception:
        logger.exception(f"❌ Ошибка при регистрации пользователя {message.from_user.full_name} ({message.from_user.id})")
        await message.answer("Произошла ошибка. Попробуйте позже.")
