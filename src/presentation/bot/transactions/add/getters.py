from typing import Any
from aiogram_dialog import DialogManager
from src.application.containers.container import Container
from src.domain.use_case.intarface import UseCaseMultipleEntities
from src.domain.entities.category import CategoryEntity


async def getter_categories(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    container: Container = cast(Container, dialog_manager.middleware_data["container"])  # type: ignore
    use_case: UseCaseMultipleEntities[CategoryEntity] = container.get_categories_uc()

    categories: list[CategoryEntity] = await use_case.execute(
        dialog_manager.event.from_user.id
    )
    dialog_manager.dialog_data["categories"] = categories  # type: ignore

    type: str = dialog_manager.dialog_data["transaction_type"]  # type: ignore
    types_transaction: dict[str, Any] = {
        "income": "доход",
        "expense": "расход",
    }

    return {
        "type_tr": types_transaction[type],
        "categories": categories,
    }
