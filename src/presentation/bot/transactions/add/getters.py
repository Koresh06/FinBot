
from aiogram_dialog import DialogManager
from src.application.containers.container import Container
from src.domain.use_case.intarface import UseCaseOneEntity


async def getter_categories(dialog_manager: DialogManager, **kwargs) -> dict:
    container: Container = dialog_manager.middleware_data["container"]
    use_case: UseCaseOneEntity = container.get_categories_uc()

    categories = await use_case.execute(dialog_manager.event.from_user.id)
    dialog_manager.dialog_data["categories"] = categories

    type: str = dialog_manager.dialog_data["transaction_type"]
    types_transaction: dict = {
        "income": "доход",
        "expense": "расход",
    }

    return {
        "type_tr": types_transaction[type],
        "categories": categories,
    }
