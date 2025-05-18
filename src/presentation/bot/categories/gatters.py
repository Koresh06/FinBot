from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput


async def cate_name_getter(dialog_manager: DialogManager, **kwargs):
    name: TextInput = dialog_manager.find("cat").get_value()

    return {"cat_name": name.capitalize()}