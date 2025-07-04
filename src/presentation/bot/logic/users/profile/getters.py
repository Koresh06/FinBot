from typing import Any, cast
from aiogram_dialog import DialogManager

from src.application.use_cases.intarface import UseCaseOneEntity
from src.domain.entities.user import UserEntity
from src.application.containers.container import Container


async def my_profile_details(
    dialog_manager: DialogManager,
    **kwargs: Any
) -> dict:
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseOneEntity[UserEntity | None] = container.get_user_uc()


    user = await use_case.execute(dialog_manager.event.from_user.id)

    return {
        "tg_id": user.tg_id,
        "username": user.username or "—",
        "full_name": user.full_name or "—",
        "monthly_budget": f"{user.monthly_budget} {user.currency}",
    }
