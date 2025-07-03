from typing import Any, cast

from aiogram_dialog import DialogManager
from src.application.containers.container import Container
from src.application.use_cases.intarface import UseCaseMultipleEntities
from src.domain.entities.category import CategoryEntity
from src.domain.value_objects.operetion_type_enum import OperationType


types_transaction: dict[str, Any] = {
    "income": "доход",
    "expense": "расход",
}


async def getter_categories(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseMultipleEntities[CategoryEntity] = container.get_categories_uc()

    type: str = dialog_manager.dialog_data["transaction_type"]

    categories: list[CategoryEntity] = await use_case.execute(
        tg_id=dialog_manager.event.from_user.id,
        type=OperationType(type)
    )
    dialog_manager.dialog_data["categories"] = categories

    return {
        "type_tr": types_transaction[type],
        "categories": categories,
    }


async def getter_confirm_transaction(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    type: str = dialog_manager.dialog_data["transaction_type"]
    total_sum: str = dialog_manager.find("total_sum").get_value()
    cat: int = dialog_manager.dialog_data["cat_id"]

    return {
        "type_tr": types_transaction[type],
        "cat": cat,
        "total_sum": total_sum,
    }
