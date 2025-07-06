from typing import Any, cast
from aiogram_dialog import DialogManager

from src.application.use_cases.intarface import UseCaseOneEntity
from src.domain.entities.user import UserEntity
from src.domain.entities.monthly_balance import MonthlyBalance
from src.application.containers.container import Container
from src.presentation.bot.lexicon.dictionaries import MONTH_NAMES_RU


async def my_profile_details(dialog_manager: DialogManager, **kwargs: Any) -> dict:
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    monthly_balance_use_case: UseCaseOneEntity[MonthlyBalance | None] = (
        container.get_monthly_balance_uc()
    )
    user_use_case: UseCaseOneEntity[UserEntity | None] = container.get_user_uc()

    data = await monthly_balance_use_case.execute(dialog_manager.event.from_user.id)
    user = await user_use_case.execute(dialog_manager.event.from_user.id)

    return {
        "tg_id": data.tg_id,
        "username": dialog_manager.event.from_user.username or "—",
        "full_name": dialog_manager.event.from_user.full_name or "—",
        "year": data.year,
        "month": MONTH_NAMES_RU[data.month],
        "income": f"{data.income:,.0f}".replace(",", " "),
        "expense": f"{data.expense:,.0f}".replace(",", " "),
        "monthly_balance": f"{data.balance:,.0f}".replace(",", " "),
        "balance": f"{user.balance:,.0f}".replace(",", " "),
        "currency": user.currency.value,
    }
