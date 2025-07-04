from typing import Any, Dict
from aiogram_dialog import DialogManager


async def cate_name_getter(dialog_manager: DialogManager,**kwargs: Any) -> Dict[str, str]:
    name: str = dialog_manager.find("cat").get_value()
    return {"cat_name": name.capitalize()}


